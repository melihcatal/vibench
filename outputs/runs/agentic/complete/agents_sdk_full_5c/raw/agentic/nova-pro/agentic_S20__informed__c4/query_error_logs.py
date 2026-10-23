import google.cloud.logging

client = google.cloud.logging.Client()
client.setup_logging()

logger = client.logger('my_logger')
filter_ = 'severity>=ERROR'
entries = logger.list_entries(filter_=filter_)
for entry in entries:
    print(entry.payload)