FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /white_stripes
ADD . /white_stripes
COPY .env_server /white_stripes/.env

CMD python manage.py migrate && python manage.py runserver --noreload 0.0.0.0:8000
