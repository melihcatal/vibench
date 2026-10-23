import os
from alibabacloud_green20180509 import Client as GreenClient
from alibabacloud_tea_openapi import models as open_api_models


def check_safety(text):
    config = open_api_models.Config(
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    client = GreenClient(config)
    request = open_api_models.OpenApiRequest({"text": text})
    response = client.image_censor_async(request)
    return response.body
