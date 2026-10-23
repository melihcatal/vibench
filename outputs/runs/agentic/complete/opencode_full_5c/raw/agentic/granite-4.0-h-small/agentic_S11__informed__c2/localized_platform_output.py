# [LATER-STEP] localized_platform_output.py

# Translate platform model output for another locale using Alibaba Machine Translation SDK
import os
import json
from alibabacloud_alimt20210318.client import Client as MtClient
from alibabacloud_alimt20210318.models import (
    TranslateTextRequest,
    TranslateTextResponseBody,
)
from model_client import get_client, PROVIDER
from model_models import ModelResponse

LOCALE_MAP = {
    "en": "en",
    "zh": "zh",
    "de": "de",
    # Add additional language codes as needed
}


def translate(text: str, target_lang: str = "zh") -> str:
    """Translate the given text to the target language code."""
    creds = {
        "access_key_id": os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        "access_key_secret": os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
        "region_id": os.getenv("ALIBABA_CLOUD_REGION", "cn-shanghai"),
    }
    mt = MtClient(**creds)
    resp: TranslateTextResponseBody = mt.translate_text(
        TranslateTextRequest(
            source_language="en",
            target_language=LOCALE_MAP.get(target_lang, "en"),
            source_text=text,
        )
    )
    return resp.translated_text  # type: ignore


# Example usage: translate a Bedrock model response
if __name__ == "__main__":
    provider_client = get_client()
    raw_resp = provider_client.invoke_endpoint(
        ModelId="arn:...", Body=json.dumps({"prompt": "Hello"})
    )
    model_resp = ModelResponse(json.loads(raw_resp["Body"].read().decode()))
    english_text = model_resp.content
    simplified = translate(english_text, target_lang="zh")
    print("Translated:", simplified)
