import os
from google.cloud import logging

def get_client():
    return logging.Client()

def get_logger(client, log_name):
    return client.logger(log_name)