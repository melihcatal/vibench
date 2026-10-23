# [LATER-STEP] live_caption_translate.py
# Translate live captions into another language using Alibaba Cloud Translation (Machine Translation)
import os
from alibabacloud_alimt20181012.client import Client
from alibabacloud_tea_openapi.models import Config
from alibabacloud_alimt20181012.models import TranslateRequest

# Provider configuration variables
ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")

# Translation target language code (ISO 639-1)
TARGET_LANG = "es"  # Example: Spanish translation

client = Client(
    Config(
        access_key_id=ALIBABA_ACCESS_KEY_ID,
        access_key_secret=ALIBABA_ACCESS_KEY_SECRET,
        endpoint="mt.cn-hangzhou.aliyuncs.com",
    )
)


async def translate_live_caption(caption):
    request = TranslateRequest(
        source_content=caption,
        source_language="auto",
        target_language=TARGET_LANG,
    )
    response = client.translate(request)
    return response.body


if __name__ == "__main__":
    # Placeholder: feed live captions here
    result = translate_live_caption("Hello, how are you?")
    print(result)
