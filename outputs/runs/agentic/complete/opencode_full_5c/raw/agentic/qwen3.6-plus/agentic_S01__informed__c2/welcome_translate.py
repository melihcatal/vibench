import os
import deepl
from typing import List, Dict, Optional

DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")
DEEPL_API_URL = "https://api-free.deepl.com"

ONBOARDING_COPY_DEFAULT = {
    "welcome_title": "Welcome to Our Platform",
    "welcome_body": "We are excited to have you join our community. Please complete your profile to get started.",
    "next_steps_title": "Getting Started",
    "next_steps_body": "Follow these simple steps to set up your account and start exploring.",
    "support_title": "Need Help?",
    "support_body": "Our support team is available 24/7 to assist you with any questions.",
}


def translate_onboarding_copy(
    target_lang: str,
    copy_map: Optional[Dict[str, str]] = None,
    formality: Optional[str] = None,
) -> Dict[str, str]:
    translator = deepl.Translator(DEEPL_AUTH_KEY, server_url=DEEPL_API_URL)
    texts = copy_map or ONBOARDING_COPY_DEFAULT
    keys = list(texts.keys())
    source_texts = list(texts.values())
    translate_kwargs: Dict[str, str] = {
        "target_lang": target_lang.upper(),
    }
    if formality:
        translate_kwargs["formality"] = formality
    results = translator.translate_text(source_texts, **translate_kwargs)
    translated = {}
    for key, result in zip(keys, results):
        translated[key] = result.text
    return translated


def translate_single_text(
    text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
) -> str:
    translator = deepl.Translator(DEEPL_AUTH_KEY, server_url=DEEPL_API_URL)
    translate_kwargs: Dict[str, str] = {
        "target_lang": target_lang.upper(),
    }
    if source_lang:
        translate_kwargs["source_lang"] = source_lang.upper()
    if formality:
        translate_kwargs["formality"] = formality
    result = translator.translate_text(text, **translate_kwargs)
    return result.text
