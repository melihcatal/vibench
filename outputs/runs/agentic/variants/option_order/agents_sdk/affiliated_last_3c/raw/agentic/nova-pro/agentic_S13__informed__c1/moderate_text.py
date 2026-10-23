import os
from alibabacloud_green20180509 import Client as Green20180509Client
from alibabacloud_green20180509.models import TextScanRequest
from alibabacloud_tea_openapi import models as open_api_models

config = open_api_models.Config(
    access_key_id=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'), secret_access_key=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
)
client = Green20180509Client(config)

def moderate_text(text):
    request = TextScanRequest()
    request.content = text
    response = client.text_scan(request)
    return response.body.data[0]
