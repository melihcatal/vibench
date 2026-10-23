import json

# Translate secret-rotation runbook notes
# Using Alibaba Cloud Machine Translation as an example
import os
from alibabacloud_alimt20210309.client import Client as AliMtClient
from alibabacloud_tea_util.model import Config as TeaConfig

ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_ACCESS_KEY_SECRET")
ALIBABA_REGION = os.getenv("ALIBABA_REGION", "cn-hangzhou")
SOURCE_LANG = "en"
TARGET_LANG = "zh"

config = TeaConfig(
    access_key_id=ALIBABA_ACCESS_KEY_ID,
    access_key_secret=ALIBABA_ACCESS_KEY_SECRET,
    region_id=ALIBABA_REGION,
)
client = AliMtClient(config)


def translate_runbook(note: str) -> str:
    """Translate secret-rotation runbook notes from source to target language.",
    Returns the translated text.
    """
    request = {
        "source_language": SOURCE_LANG,
        "target_language": TARGET_LANG,
        "content": note,
    }
    response = client.translate_content(request)
    return response.get("translated_content", "")


if __name__ == "__main__":
    note = os.getenv("RUNBOOK_NOTE")
    if note:
        print("Translated note:", translate_runbook(note))
    else:
        print("Set RUNBOOK_NOTE env var")
