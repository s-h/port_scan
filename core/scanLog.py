#!/usr/bin/env python3
import logging,os
import logging.handlers
class Logger():
    level_config={
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
    }
    def __init__(self,filename,default_level="info",when="D",backupCount=3,fmt='%(levelname)s-%(asctime)s-%(filename)s[line:%(lineno)d]-%(message)s'):
        self.logger=logging.getLogger(os.path.basename(filename))
        self.logger.setLevel(self.level_config.get(default_level))
        format_str=logging.Formatter(fmt)
        fscreen=logging.StreamHandler()
        fscreen.setFormatter(format_str)
        logfile=logging.handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backupCount,encoding='utf-8')
        logfile.setFormatter(format_str)
        self.logger.addHandler(fscreen)
        self.logger.addHandler(logfile)

def scanLog(filename, default_level="info"):
    logger = Logger(filename=filename, default_level=default_level)
    return logger.logger

if __name__ == '__main__':
    scanLog = scanLog(filename="testfile.log")
    scanLog.info("123")
    