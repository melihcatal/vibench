import os
from google.cloud import logging

client = logging.Client()
logger = client.logger("error-logs")


def query_error_logs():
    query_client = client.query(
        filter_="severity>=ERROR", order_by="timestamp desc", limit=10
    )
    for entry in query_client.run():
        print(entry.payload)


if __name__ == "__main__":
    query_error_logs()
