import os
from google.cloud import logging

client = logging.Client()


def write_log(log_name, log_data):
    logger = client.logger(log_name)
    logger.log_struct(log_data)
