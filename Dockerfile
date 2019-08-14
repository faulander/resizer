FROM python:3.7.4-alpine3.10
WORKDIR /app
COPY resizer.py /app
COPY resizer.ini /app
COPY requirements.txt /app
RUN pip install --upgrade pip
RUN apk --update add \
    build-base \
    jpeg-dev \
    zlib-dev
RUN pip install -r requirements.txt
ENV DOCKER_CONTAINER=true
VOLUME /mnt/HD2/Pr0n/Picturesets/:/New
CMD ["python", "resizer.py"]
