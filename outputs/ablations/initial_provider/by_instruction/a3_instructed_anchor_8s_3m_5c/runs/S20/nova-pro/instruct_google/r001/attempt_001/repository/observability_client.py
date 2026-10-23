from google.cloud import logging
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/service-account-file.json'

def get_client():
    return logging.Client()

def get_logger(client, log_name):
    return client.logger(log_name)