import os
from google.cloud import logging


def get_observability_client():
    client = logging.Client()
    return client


def get_logger(client, logger_name):
    logger = client.logger(logger_name)
    return logger
