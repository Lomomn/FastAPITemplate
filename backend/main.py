import os
import json
from passlib.hash import pbkdf2_sha256
from fastapi import FastAPI
from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase
import playhouse.signals as Signal

###############################################################################
# Database Init
###############################################################################
db = PostgresqlExtDatabase(
  os.environ['POSTGRES_DB'],
  host = 'db',
  user = os.environ['POSTGRES_USER'],
  password = os.environ['POSTGRES_PASSWORD']
)

# Models
class BaseExtModel(Signal.Model):
  class Meta:
    database = db


class Person:
  class PersonModel(BaseExtModel):
    name = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    
    def __str__(self):
      return '😎 PersonModel:\n\tname: {}\n\temail: {}\n\tpassword: {}'.format(
        self.name, self.email, self.password
      )
  
  @Signal.pre_save(sender=PersonModel)
  def pre_save_handler(sender, instance, created):
    # Hash the password before save
    instance.password = pbkdf2_sha256.hash(instance.password)
    print('👉 verify: ', pbkdf2_sha256.verify('oops', instance.password))


class Product:
  class ProductModel(BaseExtModel):
    name = CharField()
    description = TextField()


class Project:
  class ProjectModel(BaseExtModel):
    title = CharField()
    author = ForeignKeyField(
      Person.PersonModel,
      backref='projects',
      on_update='cascade',
      on_delete='cascade'
    )

db.connect()
db.drop_tables([Product.ProductModel, Project.ProjectModel, Person.PersonModel])
db.create_tables([Person.PersonModel, Product.ProductModel, Project.ProjectModel])
for person in Person.PersonModel.select():
    print('🔍 ', person.name, person.email, person.password)

# 🙏 Create the admin account
try:
  admin = Person.PersonModel(
    name='admin',
    email='hello@example.com',
    password='oops'
  )
  print('👍 Admin account saved!', admin.save())
except IntegrityError as e:
  print('👎 Admin already saved!', e)

print(admin)
db.close()

###############################################################################
# FastAPI Routes
###############################################################################
app = FastAPI()

@app.get("/api")
def read_root():
  return {"Hello": "World"}


@app.get("/api/items/{item_id}")
def read_item(item_id: int, q: str = None):
  return {"item_id": item_id, "q": q}
