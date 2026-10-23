import os
from google.cloud import logging

client = logging.Client()


def get_client():
    return client


def get_log_name():
    return "my-log"
