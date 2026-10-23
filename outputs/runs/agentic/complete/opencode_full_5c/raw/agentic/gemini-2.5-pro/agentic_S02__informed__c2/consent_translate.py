import os
import deepl
from typing import Optional


def translate_consent_text(text: str, target_language: str = "FR") -> Optional[str]:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        print(f"Error during translation: {e}")
        return None


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    consent_text = (
        "By continuing, you agree to our terms of service and privacy policy."
    )

    print(f"Original (EN): {consent_text}")

    translated_fr = translate_consent_text(consent_text, "FR")
    if translated_fr:
        print(f"Translated (FR): {translated_fr}")

    translated_es = translate_consent_text(consent_text, "ES")
    if translated_es:
        print(f"Translated (ES): {translated_es}")

    translated_ja = translate_consent_text(consent_text, "JA")
    if translated_ja:
        print(f"Translated (JA): {translated_ja}")
