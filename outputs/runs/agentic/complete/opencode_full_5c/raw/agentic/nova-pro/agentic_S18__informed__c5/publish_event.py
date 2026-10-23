import os
from google.cloud import pubsub_v1

# Set up the publisher client
publisher = pubsub_v1.PublisherClient()

# Set the name of the topic
topic_name = "your-topic-name"

# The data to publish
data = b'{"event": "sample_event"}'
