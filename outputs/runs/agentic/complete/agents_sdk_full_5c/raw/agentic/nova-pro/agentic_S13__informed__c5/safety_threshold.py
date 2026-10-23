from alibabacloud_green20180509 import Client as GreenClient
from alibabacloud_tea_openapi import models as open_api_models

config = open_api_models.Config(
    access_key_id='ALIBABA_CLOUD_ACCESS_KEY_ID',
    access_key_secret='ALIBABA_CLOUD_ACCESS_KEY_SECRET'
)
client = GreenClient(config)

def safety_threshold(text):
    response = client.image_scan(text)
    return response.body
