FROM python:3.12
WORKDIR /app
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y netcat && apt-get clean
COPY requirements.txt ./
RUN pip3 install mysqlclient
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD python manage.py runserver
