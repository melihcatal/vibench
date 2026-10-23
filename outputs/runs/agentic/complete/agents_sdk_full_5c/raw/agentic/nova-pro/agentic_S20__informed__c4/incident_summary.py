import google.cloud.logging

client = google.cloud.logging.Client()
client.setup_logging()

logger = client.logger('my_logger')
filter_ = 'severity>=ERROR'
entries = logger.list_entries(filter_=filter_)
summary = '\n'.join([entry.payload for entry in entries])
print(summary)