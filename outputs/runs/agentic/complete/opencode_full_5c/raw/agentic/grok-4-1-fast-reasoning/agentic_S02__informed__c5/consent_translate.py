import os
from deepl import Translator


def translate_identity_consent(text: str, target_lang: str = "EN") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text


if __name__ == "__main__":
    sample_consent = "By logging in, you agree to our terms."
    print(translate_identity_consent(sample_consent, "ES"))
