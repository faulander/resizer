import configparser
import os
import sys
from loguru import logger
import multiprocessing
from PIL import Image
import schedule
import time


def processImages(pathtoprocess):
    logger.info("Unwanted files: {}", lstUnwantedExtensions)
    lstResizeImages = list()
    for path, subdir, files in os.walk(pathtoprocess):
        logger.info("processing: {}", path)
        for fname in files:
            if fname.endswith(".jpg") or fname.endswith(".jpeg"):
                fullpath = os.path.join(path, fname)
                lstResizeImages.append(fullpath)
            for extension in lstUnwantedExtensions:
                if fname.endswith(extension):
                    os.remove(os.path.join(path, fname))
                    logger.info("File deleted: {}", os.path.join(path, fname))
    if len(lstResizeImages) > 0:
        pool = multiprocessing.Pool()
        pool.map(resizeImage, lstResizeImages)
        pool.close()
    else:
        logger.info("No new pictures found for processing.")


def resizeImage(image, maxsize=3500):
    try:
        bild = Image.open(image)
        bild.thumbnail((maxsize, maxsize), Image.ANTIALIAS)
        outfile = os.path.splitext(image)[0] + ".jpg"
        bild.save(outfile, "JPEG")
    except IOError:
        logger.error("Error on file {}", image)
    try:
        outfile = os.path.splitext(image)[0] + ".jpg"
        bild.save(outfile, "JPEG")
        logger.info("File processed: {}", outfile)
    except IOError:
        logger.error("Error on file {}", outfile)


def job():
    processImages(cfgInputPath)



if __name__ == '__main__':
    schedule.every().day.at("12:00").do(job)
    #logger.add(sys.stdout, format="{time} - {level} - {message}", level="INFO")
    config = configparser.ConfigParser(allow_no_value=True)
    config.read("resizer.ini")
    SECRET_KEY = os.environ.get('DOCKER_CONTAINER', False)
    if SECRET_KEY:
        logger.info("Script runs in an DOCKER Environment")
        cfgInputPath = config["RESIZER"]["inputpath"]
    else:
        logger.info("Script does not run in DOCKER Environment")
        cfgInputPath = "/home/harald/Europa/HD2/Pr0n/Picturesets/"
    lstUnwantedExtensions = (config["RESIZER"]["unwantedextensions"]).split(",")
    while True:
        schedule.run_pending()
        time.sleep(1)
    # processImages(cfgInputPath)
