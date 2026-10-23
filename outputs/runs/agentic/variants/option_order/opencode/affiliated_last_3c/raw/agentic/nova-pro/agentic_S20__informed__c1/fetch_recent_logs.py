import os
from google.cloud import logging

client = logging.Client()


def fetch_recent_logs(log_name, field, value, start_time, end_time):
    logger = client.logger(log_name)
    filter_ = (
        f'{field}={value} AND timestamp >= "{start_time}" AND timestamp <= "{end_time}"'
    )
    entries = logger.list_entries(filter_=filter_)
    return [entry.payload for entry in entries]
