# invoice_note_translate.py
# [LATER-STEP]
# Translate extracted invoice notes or descriptions using Alibaba Cloud Machine Translation.

import json
from alibabacloud_alimt20191001.client import Client as AlimtClient
from alibabacloud_tea_openapi.models import Config
from alibabacloud_oss_util import get_default_region

# Alibaba Cloud credentials
access_key_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
access_key_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")

# Build auth configuration
config = Config(
    access_key_id=access_key_id,
    access_key_secret=access_key_secret,
    # Use default region; adjust if needed
    region_id=get_default_region(),
)
client = AlimtClient(config)


def translate_note(note: str, target_lang: str = "en") -> str:
    """Translate a free‑text note from source language to target language.

    Args:
        note: The source note string.
        target_lang: ISO‑639‑1 target language (default English).

    Returns:
        Translated note.
    """
    response = client.translate(
        SourceText=note,
        SourceLanguage="auto",
        TargetLanguage=target_lang,
    )
    # Response shape: {"Translated": "Your translated text"}
    return response.body.Translated


# Example usage
if __name__ == "__main__":
    sample_note = "请检查本发票的发货地址是否正确。"
    translated = translate_note(sample_note, target_lang="en")
    print(json.dumps({"translated": translated}, indent=2))
