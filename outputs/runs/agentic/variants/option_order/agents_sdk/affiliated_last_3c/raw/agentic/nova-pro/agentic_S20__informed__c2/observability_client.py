import os
from google.cloud import logging

def get_logger(logger_name):
    client = logging.Client()
    return client.logger(logger_name)