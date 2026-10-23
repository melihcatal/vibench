import os
import deepl


def translate_consent_text_with_deepl(text: str, target_language: str = "DE"):
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        print(f"An error occurred during translation: {e}")
        return None


if __name__ == "__main__":
    consent_text_en = "By proceeding, you agree to share your profile information including your email address and full name with our application."

    print(f"Original (EN): {consent_text_en}")

    try:
        translated_text_de = translate_consent_text_with_deepl(consent_text_en, "DE")
        if translated_text_de:
            print(f"Translated (DE): {translated_text_de}")

        translated_text_fr = translate_consent_text_with_deepl(consent_text_en, "FR")
        if translated_text_fr:
            print(f"Translated (FR): {translated_text_fr}")

    except ValueError as e:
        print(e)
