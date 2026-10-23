# [LATER-STEP] welcome_translate.py
# Translate onboarding copy into the user's locale using Alibaba Cloud Machine Translation

import os
from alibabacloud_alimt20181011.client import Client as AliMTClient
from alibabacloud_tea_util_0_0_1.models import RuntimeOptions
from alibabacloud_alimt20181011.models import TranslateRequest

ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
REGION = os.getenv("ALIBABA_CLOUD_REGION", "cn-hangzhou")


def translate_welcome(text: str, target_lang: str = "en") -> str:
    """Translate onboarding welcome message to target language."""
    client = AliMTClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, region=REGION)
    req = TranslateRequest(
        source_language="zh",
        target_language=target_lang,
        source_text=text,
    )
    runtime = RuntimeOptions()
    response = client.translate(req, runtime)
    return response.body.target_text


# End of file
