import os
import json
import urllib.parse
import urllib.request


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def translate_welcome_copy(text: str, target_lang: str, source_lang: str = "EN") -> str:
    api_key = os.environ["DEEPL_AUTH_KEY"]
    data = urllib.parse.urlencode(
        {
            "auth_key": api_key,
            "text": text,
            "source_lang": source_lang,
            "target_lang": target_lang.upper(),
        }
    ).encode("utf-8")
    request = urllib.request.Request(DEEPL_API_URL, data=data, method="POST")
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload["translations"][0]["text"]


def translate_onboarding_copy(user_locale: str) -> str:
    onboarding_copy = "Welcome! Let's get started with your setup."
    locale = user_locale.split("-")[0].upper()
    return translate_welcome_copy(onboarding_copy, locale)
