import os
import alibabacloud_green20180509 as green
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_green20180509.models import TextScanRequest

ALIBABA_CLOUD_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_CLOUD_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")


def redact_unsafe(text):
    config = green.Config(
        access_key_id=ALIBABA_CLOUD_ACCESS_KEY_ID,
        access_key_secret=ALIBABA_CLOUD_ACCESS_KEY_SECRET,
    )
    client = green.Client(config)
    request = TextScanRequest()
    request.text = text
    response = client.text_scan(request)
    return response.body.data[0].results[0].suggestion
