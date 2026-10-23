import os
from google.cloud import logging

client = logging.Client()
logger = client.logger("incident-summary")


def summarize_error_logs():
    query_client = client.query(
        filter_="severity>=ERROR", order_by="timestamp desc", limit=10
    )
    summary = []
    for entry in query_client.run():
        summary.append(entry.payload)
    return summary


if __name__ == "__main__":
    print(summarize_error_logs())
