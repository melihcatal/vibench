# localized_platform_output.py
"""Translate platform model output for another locale using Alibaba Machine Translation SDK.
The function takes the generated text, source language code, and target language code,
and returns the translated text together with original metadata.
"""

import os
import json
from alibabacloud_alimt20230725.client import Client as MtClient
from alibabacloud_alimt20230725.models import TranslateTextRequest
from model_models import ProviderInfo, ApiResponse


def translate(text: str, source_lang: str = "en", target_lang: str = "zh-CN", provider_info: ProviderInfo = None) -> Dict[str, Any]:
    """Translate generated text using Alibaba Cloud Machine Translation.

    Returns a dict containing original text, target text, and provider metadata.
    """
    client = MtClient(endpoint="mts.cn-hangzhou.aliyuncs.com",
                      access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
                      access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"))
    request = TranslateTextRequest(
        source_lang=source_lang,
        target_lang=target_lang,
        source_text=text
    )
    response = client.translate_text(request)
    result = response.result()
    # Alibaba returns a JSON with \"translatedText\" field
    translation = result.get('translatedText') or ""
    return {
        "source": text,
        "target": translation,
        "metadata": provider_info.__dict__ if provider_info else {}
    }

if __name__ == "__main__":
    import argparse, json
    parser = argparse.ArgumentParser(description="Translate model output")
    parser.add_argument("text", help="Generated text")
    parser.add_argument("--src", default="en", help="Source language code (default en)")
    parser.add_argument("--dst", default="zh-CN", help="Target language code (default zh-CN)")
    args = parser.parse_args()
    print(json.dumps(translate(args.text, args.src, args.dst), indent=2))
