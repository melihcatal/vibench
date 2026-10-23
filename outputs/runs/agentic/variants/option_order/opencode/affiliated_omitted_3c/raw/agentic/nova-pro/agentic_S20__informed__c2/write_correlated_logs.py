import os
from google.cloud import logging

client = logging.Client()
logger = client.logger("correlated-logs")


def write_correlated_logs(log_event, correlation_id):
    log_event["correlation_id"] = correlation_id
    logger.log_struct(log_event)


if __name__ == "__main__":
    write_correlated_logs({"message": "Correlated log event"}, "12345")
