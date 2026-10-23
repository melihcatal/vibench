from google.cloud import logging


def query_error_logs(log_name, filter_, order_by):
    client = logging.Client()
    logger = client.logger(log_name)
    entries = logger.list_entries(filter_=filter_, order_by=order_by)
    for entry in entries:
        print(entry.payload)
    print(f"Queried error logs from {log_name}")
