from google.cloud import logging

def summarize_message_processing(project_id, log_name, resource, message):
    client = logging.Client()
    logger = client.logger(log_name)
    logger.log_struct(message, resource=resource)