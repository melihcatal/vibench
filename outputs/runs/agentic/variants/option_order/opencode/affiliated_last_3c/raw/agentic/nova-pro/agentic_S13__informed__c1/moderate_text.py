import os

from alibabacloud_green import Client as GreenClient
from alibabacloud_green.requests import CreateScanRequest
from alibabacloud_green.config import Config

# Initialize the client
config = Config()
config.access_key_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
config.access_key_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
client = GreenClient(config)


def moderate_text(text):
    request = CreateScanRequest()
    request.content = text
    response = client.create_scan(request)
    return response
