import os
import google.cloud.logging


def get_client():
    client = google.cloud.logging.Client()
    client.setup_logging()
    return client


def get_logger(client, log_name):
    return client.logger(log_name)
