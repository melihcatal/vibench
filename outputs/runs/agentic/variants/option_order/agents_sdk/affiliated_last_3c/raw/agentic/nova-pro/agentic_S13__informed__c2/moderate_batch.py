import os
from alibabacloud_green20180509 import models as green_models
from alibabacloud_green20180509.client import Client as GreenClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient

def moderate_batch(texts):
    config = open_api_models.Config(
        access_key_id=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    )
    client = GreenClient(config)
    results = []
    for text in texts:
        request = green_models.ImageScanRequest()
        request.image_url = text
        response = client.image_scan(request)
        results.append(response)
    return results