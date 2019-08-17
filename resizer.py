import configparser
import os
from loguru import logger
from PIL import Image
import schedule
import time
from peewee import *


db = SqliteDatabase('images.db')


class Bild(Model):
    fullpath = CharField(unique=True)
    processed = BooleanField(default=False)

    class Meta:
        database = db 


def processPath(pathtoprocess):
    numProcess = 0
    numTotal = 0
    logger.info("Unwanted files: {}", lstUnwantedExtensions)
    for path, subdir, files in os.walk(pathtoprocess):
        # logger.info("processing: {}", path)
        for fname in files:
            fullpath = os.path.join(path, fname)
            dpath = fullpath.lstrip(pathtoprocess)
            for extension in lstUnwantedExtensions:
                # Delete unwanted files
                if fname.endswith(extension):
                    os.remove(fullpath)
                    logger.info("File deleted: {}", dpath)
            # Resize images
            if fname.endswith(".jpg") or fname.endswith(".jpeg"):
                numTotal += 1
                _, created = Bild.get_or_create(fullpath=dpath)
                if created:
                    numProcess += 1
        logger.info("Path: {} ({}/{})", str(path), str(numProcess), str(numTotal))
        numProcess = 0


def resizeImage(image, maxsize=3500):
    dpath = image.lstrip(cfgInputPath)
    try:
        bild = Image.open(image)
        width, height = bild.size
        if not (width <= maxsize) or (height <= maxsize):
            bild.thumbnail((maxsize, maxsize), Image.ANTIALIAS)
            outfile = os.path.splitext(image)[0] + ".jpg"
            bild.save(outfile, "JPEG")
            logger.info("Image resized: {}", dpath)
        else:
            logger.info("Image skipped: {}", dpath)
    except IOError:
        logger.error("Error on file {}", image)
    query = Bild.update(processed=True).where(Bild.fullpath == dpath)
    query.execute()


def processImages():
    for bild in Bild.select().where(Bild.processed == False):
        imageFull = os.path.join(cfgInputPath, bild.fullpath)
        resizeImage(imageFull)


def job():
    processPath(cfgInputPath)
    processImages()


if __name__ == '__main__':
    db.connect()
    db.create_tables([Bild], safe=True)
    config = configparser.ConfigParser(allow_no_value=True)
    config.read("resizer.ini")
    SECRET_KEY = os.environ.get('DOCKER_CONTAINER', False)
    lstUnwantedExtensions = (config["RESIZER"]["unwantedextensions"]).split(",")
    if SECRET_KEY:
        logger.info("Script runs in an DOCKER Environment")
        cfgInputPath = config["RESIZER"]["inputpath"]
        schedule.every().day.at("22:00").do(job)
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        logger.info("Script does not run in DOCKER Environment")
        cfgInputPath = "/home/harald/Europa/HD2/Pr0n/Picturesets/"
        job()
