import google.cloud.logging

client = google.cloud.logging.Client()
client.setup_logging()

logger = client.logger('my_logger')
logger.log_struct({'event': 'structured_log_event'})