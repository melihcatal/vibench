import os
import deepl


def translate_text(text: str, target_language: str = "en") -> str:
    """
    Translates text using the DeepL API.

    Args:
        text: The text to translate.
        target_language: The target language code (e.g., "en" for English, "fr" for French).
                         See DeepL API documentation for supported languages.

    Returns:
        The translated text.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except Exception as e:
        print(f"Error translating text with DeepL: {e}")
        raise


if __name__ == "__main__":
    # Example Usage (replace with actual values)
    TEXT_TO_TRANSLATE = os.environ.get(
        "TEXT_TO_TRANSLATE", "Guten Tag, wie geht es Ihnen?"
    )
    TARGET_LANGUAGE = os.environ.get("TARGET_LANGUAGE", "en")

    if TEXT_TO_TRANSLATE == "Guten Tag, wie geht es Ihnen?" and TARGET_LANGUAGE == "en":
        print(
            "Please set TEXT_TO_TRANSLATE and TARGET_LANGUAGE environment variables or update script."
        )
    else:
        print(f"Translating '{TEXT_TO_TRANSLATE}' to '{TARGET_LANGUAGE}'...")
        translated_text = translate_text(TEXT_TO_TRANSLATE, TARGET_LANGUAGE)
        print("Translated Text:")
        print(translated_text)
