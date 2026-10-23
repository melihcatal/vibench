import os
from typing import Dict, Any

# Alibaba Machine Translation example
# Use the alibabacloud_alimt SDK

# Expected environment variables: ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET


def translate_text(
    source_text: str, source_lang: str = "en", target_lang: str = "zh"
) -> str:
    """Translate a single text string between languages using Alibaba Machine Translation.

    Args:
        source_text: The text to translate.
        source_lang: Language code of the source (default "en").
        target_lang: Language code of the target (default "zh").

    Returns:
        Translated text.
    """
    from alibabacloud_alimt20200323.client import Client

    # Configure the Alibaba Cloud client
    client = Client(
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
        endpoint="mt.cn-hangzhou.aliyuncs.com",
    )

    # Prepare the request payload
    request = {
        "SourceText": source_text,
        "SourceLanguage": source_lang,
        "TargetLanguage": target_lang,
        "Category": "general",  # generic text translation category
    }

    # Call the SDK method for translation
    response = client.mt_translate(request)

    # Extract the translated text (adjust key path if SDK differs)
    translated = response.get("TargetText", "Translation failed")
    return translated


# Simple test harness when run directly
if __name__ == "__main__":
    sample = "Hello, world!"
    print(f"Original: {sample}")
    print(f"Translated: {translate_text(sample)}")
