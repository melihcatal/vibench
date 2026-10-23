import os
import alibabacloud_alimt20240715
from alibabacloud_alimt20240715.client import Client
from typing import Any, Dict

# Alibaba Cloud credentials from env
ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")

TRANSLATION_ENDPOINT = "cn-beijing.alimt.aliyuncs.com"  # example region

# Create a client once (singleton pattern)
_alimt_client: Client | None = None

def _get_alimt_client() -> Client:
    global _alimt_client
    if _alimt_client is None:
        _alimt_client = Client(
            access_key_id=ALIBABA_ACCESS_KEY_ID,
            access_key_secret=ALIBABA_ACCESS_KEY_SECRET,
            endpoint=TRANSLATION_ENDPOINT,
            region_id="cn-beijing"
        )
    return _alimt_client

# Supported target languages for Alibaba MT (example list)
SUPPORTED_TARGETS = {"en", "ja", "ko", "de", "fr"}


def translate_output(output: str, target_lang: str = "en") -> str:
    """Translate model-generated output to a target language.

    Uses Alibaba Cloud Machine Translation service.
    Args:
        output (str): Text to translate.
        target_lang (str): ISO language code, must be in SUPPORTED_TARGETS.
    Returns:
        str: Translated text.
    Raises:
        ValueError: If target language is not supported.
    """
    if target_lang not in SUPPORTED_TARGETS:
        raise ValueError(f"Unsupported target language: {target_lang}")
    client = _get_alimt_client()
    request = alibabacloud_alimt20240715.models.TranslateTextRequest(
        source_language="auto",
        target_language=target_lang,
        source_text=output,
    )
    response = client.translate_text(request)
    # response has field 'translated_text'
    return response.translated_text

# Example usage
# if __name__ == "__main__":
#     print(translate_output("Bonjour le monde", target_lang="en"))
