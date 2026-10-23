# welcome_translate.py
# Translate onboarding copy into the user's locale (Alibaba Machine Translation reference)

import os
import json
from typing import Dict, Any

from alibabacloud_alimt20240724.client import Client as AliMTClient
from alibabacloud_tea_openapi.models import Config
from identity_models import RegisterUserRequest

# Alibaba Cloud credentials (set as environment variables)
ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
if not ALIBABA_ACCESS_KEY_ID or not ALIBABA_ACCESS_KEY_SECRET:
    raise RuntimeError(
        "Set ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET"
    )

# Create MT client
config = Config(
    access_key_id=ALIBABA_ACCESS_KEY_ID,
    access_key_secret=ALIBABA_ACCESS_KEY_SECRET,
    region_id="ap-southeast-1",
)
mt_client = AliMTClient(config)


def translate_onboarding(request: RegisterUserRequest) -> Dict[str, Any]:
    """Translate the user's onboarding notes from source language to target language.
    Here we assume source is English and target is the user's locale extracted from the request.
    """
    source_lang = "en"
    target_lang = (
        request.notes.split()[0].upper() if request.notes else "EN"
    )  # naive extraction
    text = request.notes or "Welcome to our service!"
    response = mt_client.translate_text(
        SourceLanguage=source_lang,
        TargetLanguage=target_lang,
        SourceText=text,
    )
    result = response.to_dict()
    return {
        "translated_text": result.get("TargetText"),
        "source_language": source_lang,
        "target_language": target_lang,
    }


# Example usage (do not run in production script)
if __name__ == "__main__":
    user = RegisterUserRequest(
        email="alice@example.com",
        password="P@ssw0rd!",
        notes="Welcome to our service! We're glad you're here.",
    )
    translation = translate_onboarding(user)
    print(json.dumps(translation, indent=2))
