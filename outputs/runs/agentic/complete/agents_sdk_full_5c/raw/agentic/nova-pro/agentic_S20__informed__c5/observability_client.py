import os
from google.cloud import logging

def get_logging_client():
    return logging.Client()

def get_logger(client, logger_name):
    return client.logger(logger_name)