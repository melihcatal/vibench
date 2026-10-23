import os
from alibabacloud_green import Green


def corpus_safety(text: str) -> bool:
    access_key_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    access_key_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if not access_key_id or not access_key_secret:
        raise ValueError(
            "ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET environment variables not set"
        )
    client = Green(access_key_id, access_key_secret)
    response = client.text_scan(text)
    return response["data"]["results"][0]["label"] == "PASS"
