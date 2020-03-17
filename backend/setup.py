import io

from setuptools import find_packages, setup

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='template',
    version='1.0.0',
    license='BSD',
    description='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'uvicorn',          # ASGI server
        'fastapi',          # Web framework
        'psycopg2-binary',  # Postgres driver
        'peewee',           # ORM
        'passlib'           # Password hashing library
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage'
        ],
    },
)