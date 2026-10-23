from google.cloud import logging


def write_structured_log(log_name, resource, labels, log_entry):
    client = logging.Client()
    logger = client.logger(log_name)
    logger.log_struct(log_entry, resource=resource, labels=labels)
    print(f"Logged entry to {log_name}")
