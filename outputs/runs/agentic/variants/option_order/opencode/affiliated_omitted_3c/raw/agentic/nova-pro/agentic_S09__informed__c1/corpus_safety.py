import os
from alibabacloud_green import GreenClient

client = GreenClient(
    access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
    access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
)


def check_corpus_safety(text: str) -> bool:
    response = client.scan_text(text=text)
    return response["is_safe"]
