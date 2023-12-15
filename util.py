import logging
from settings import settings


verboseprint = print if settings["verbose"] else lambda *a, **k: None

def infomessage(logger,str):
    verboseprint("intraupdate:",str)
    logger.info(str)