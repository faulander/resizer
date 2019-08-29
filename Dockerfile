FROM python:3.6.9-slim-buster
WORKDIR /app
COPY resizer.py /app
COPY resizer.ini /app
COPY requirements.txt /app
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev
RUN pip install -r requirements.txt
ENV DOCKER_CONTAINER=true
CMD ["python", "resizer.py"]
