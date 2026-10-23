import os
from google.cloud import logging

client = logging.Client()


def query_error_logs(log_name, severity, start_time, end_time):
    logger = client.logger(log_name)
    filter_ = f'severity={severity} AND timestamp >= "{start_time}" AND timestamp <= "{end_time}"'
    entries = logger.list_entries(filter_=filter_)
    return [entry.payload for entry in entries]
