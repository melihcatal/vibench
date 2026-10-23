import os
import deepl
from security_models import TranslatedRunbook


def translate_runbook_notes(text: str, target_lang: str = "DE") -> TranslatedRunbook:
    """
    Translates secret-rotation runbook notes using the DeepL API.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)

        return TranslatedRunbook(
            original_text=text, translated_text=result.text, target_language=target_lang
        )
    except deepl.DeepLException as e:
        print(f"An error occurred during translation: {e}")
        return None


if __name__ == "__main__":
    runbook_text_en = "In case of rotation failure, immediately revert to the previous secret version (AWSPREVIOUS) and notify the on-call security engineer."

    translated_runbook = translate_runbook_notes(runbook_text_en, target_lang="ES")

    if translated_runbook:
        print(f"Original ({'en'}): {translated_runbook.original_text}")
        print(
            f"Translated ({translated_runbook.target_language}): {translated_runbook.translated_text}"
        )
    else:
        print("Translation failed.")
