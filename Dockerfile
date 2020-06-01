FROM python:3.8
RUN mkdir /code/
COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt
ADD . /code/localstack-example
WORKDIR /code/localstack-example/localstack_2464_example
