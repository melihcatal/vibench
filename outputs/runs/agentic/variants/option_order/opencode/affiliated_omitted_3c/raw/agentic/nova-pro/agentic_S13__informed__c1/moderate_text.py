import os

from alibabacloud_green20180509 import Client as GreenClient
from alibabacloud_green20180509.models import TextScanRequest
from alibabacloud_tea_util.models import RuntimeOptions


def moderate_text(text):
    ali_cloud_access_key_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    ali_cloud_access_key_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")

    client = GreenClient(ali_cloud_access_key_id, ali_cloud_access_key_secret)
    request = TextScanRequest()
    request.text_list = [text]
    request.scenes = ["AD", "PORN", "TERRORISM"]
    response = client.text_scan(request)
    return response
