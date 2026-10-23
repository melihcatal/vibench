import os
from google.cloud import logging

def get_logger(logger_name):
    return logging.Client().logger(logger_name)
