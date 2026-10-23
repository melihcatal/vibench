import os
from alibabacloud_green.client import Client as GreenClient
from alibabacloud_green20180509.models import TextScanRequest


def check_corpus_text(text: str) -> bool:
    client = GreenClient(
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    request = TextScanRequest(content=text)
    response = client.text_scan(request)
    return response.data.results[0].label == "pass"
