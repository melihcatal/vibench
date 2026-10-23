
import os
import deepl

def translate_text(text: str, target_language: str = "FR") -> str:
    """
    Translates text to the target language using the DeepL API.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        print(f"An error occurred during translation: {e}")
        return f"Error: Translation failed - {e}"

if __name__ == '__main__':
    # This is an example, not part of the required functionality.
    if os.getenv("DEEPL_AUTH_KEY"):
        english_text = "Hello, world! This is a test of the translation service."
        french_translation = translate_text(english_text, "FR")
        print(f"English: {english_text}")
        print(f"French: {french_translation}")

        spanish_translation = translate_text(english_text, "ES")
        print(f"Spanish: {spanish_translation}")
