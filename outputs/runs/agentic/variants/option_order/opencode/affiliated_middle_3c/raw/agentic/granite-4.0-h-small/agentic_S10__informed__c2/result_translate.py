# Translate generated text using Alibaba Machine Translation SDK

import os
from alibabacloud_alimt20200331 import client as mt_client
from alibabacloud_tea_openapi import models as open_api_models
from model_client import normalize_response

# -------------------------------------------------
# Alibaba Machine Translation client configuration
# -------------------------------------------------
ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
REGION_ID = os.getenv("ALIBABA_CLOUD_REGION_ID", "cn-hangzhou")

config = open_api_models.Config(
    access_key_id=ALIBABA_ACCESS_KEY_ID,
    access_key_secret=ALIBABA_ACCESS_KEY_SECRET,
    region_id=REGION_ID,
)
client = mt_client.Client(config)


def translate_text(source_text: str, target_lang: str = "en") -> str:
    """Translate text using Alibaba Machine Translation API."""
    response = client.translate_content(
        TranslateContentRequest={
            "SourceLanguage": "auto",
            "TargetLanguage": target_lang,
            "SourceContent": source_text,
        }
    )
    translated = response.dict().get("Data", {}).get("TranslatedContent", "")
    return translated


# Example (uncomment to test)
# result = translate_text("Bonjour!", target_lang="en")
# print(result)
