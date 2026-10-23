import os
from google.cloud import logging

client = logging.Client()
logger = client.logger("structured-log")


def write_structured_log(log_event):
    logger.log_struct(log_event)


if __name__ == "__main__":
    write_structured_log({"message": "Structured log event"})
