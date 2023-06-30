FROM python:3.10.3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip cache purge
RUN pip install poetry==1.3.2
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
