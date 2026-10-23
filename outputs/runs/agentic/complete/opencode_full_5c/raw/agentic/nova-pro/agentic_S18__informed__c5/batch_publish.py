import os
from alibabacloud_mns20150606 import Client as MnsClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_mns20150606.models import BatchSendMessageRequest

# Initialize the client
config = open_api_models.Config(
    access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
    access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
)
client = MnsClient(config)

# Set the name of the queue
queue_name = "your-queue-name"

# Create a batch message request
request = BatchSendMessageRequest()
request.queue_name = queue_name
request.messages = '{"Message":[{"Body":"message1"},{"Body":"message2"}]}'

# Send the batch message
response = client.batch_send_message(request)
