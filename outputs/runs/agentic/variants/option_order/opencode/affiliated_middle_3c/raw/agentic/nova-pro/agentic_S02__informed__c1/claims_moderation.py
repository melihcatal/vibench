import os
from alibabacloud_green20180712 import models as green_models
from alibabacloud_green20180712.client import Client as GreenClient
from alibabacloud_tea_openapi import models as open_api_models

# Configuration
config = open_api_models.Config(
    access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
    access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
)
client = GreenClient(config)


# Moderate free-text claims or notes
def moderate_claims(text):
    request = green_models.ImageScanRequest()
    request.data_id = "test"
    request.tasks = [{"task_type": "ANTI_SPAM", "content": text}]
    response = client.image_scan(request)
    return response.body.results[0].suggestion
