FROM python:3.7

WORKDIR /backend
COPY . /backend
RUN pip install --no-cache-dir -e .
# RUN pip install '.[test]'

WORKDIR /backend
CMD uvicorn main:app --reload --host 0.0.0.0 --port 8000