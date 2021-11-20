import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

def info(message: str):
  
  if type(message) is not str:
    message = str(message)

  logging.info(message)

def error(message: str):
  
  if type(message) is not str:
    message = str(message)

  logging.error(message)