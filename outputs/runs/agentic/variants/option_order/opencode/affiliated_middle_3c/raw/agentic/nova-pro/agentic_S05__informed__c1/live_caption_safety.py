from alibabacloud_green20180509.client import Client as GreenClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_green20180509 import models as green_models

config = open_api_models.Config(
    access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
    access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
)
client = GreenClient(config)


def live_caption_safety(text):
    request = green_models.TextScanRequest(
        tasks=[green_models.TextScanTask(content=text)]
    )
    response = client.text_scan(request)
    return response.body.data[0].results[0].label
