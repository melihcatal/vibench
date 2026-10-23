from google.cloud import logging


def write_correlated_logs(log_name, resource, labels, log_entries):
    client = logging.Client()
    logger = client.logger(log_name)
    for log_entry in log_entries:
        logger.log_struct(log_entry, resource=resource, labels=labels)
    print(f"Logged correlated entries to {log_name}")
