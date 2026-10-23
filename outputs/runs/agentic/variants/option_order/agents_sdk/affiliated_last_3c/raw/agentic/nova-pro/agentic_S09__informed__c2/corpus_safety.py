import os
from alibabacloud_green20180509.client import Client as GreenClient
from alibabacloud_tea_openapi import models as open_api_models

def check_corpus_safety(text):
    config = open_api_models.Config(
        access_key_id=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    )
    client = GreenClient(config)
    request = green20180509_models.TextScanRequest(content=text)
    response = client.text_scan(request)
    return response.body.results[0].suggestion