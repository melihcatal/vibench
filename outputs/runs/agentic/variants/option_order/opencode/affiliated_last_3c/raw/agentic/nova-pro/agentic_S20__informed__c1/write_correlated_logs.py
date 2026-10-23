import os
from google.cloud import logging

client = logging.Client()


def write_correlated_logs(log_name, log_data, correlation_id):
    log_data["correlation_id"] = correlation_id
    logger = client.logger(log_name)
    logger.log_struct(log_data)
