import os
from typing import Optional

from observability_client import ClientFactory

def translate_dashboard_note(
    text: str, target_language_code: str = "DE"
) -> Optional[str]:
    """
    Translates a metric or dashboard note into another locale using the DeepL API.

    Args:
        text: The text to be translated.
        target_language_code: The target language code (e.g., "DE" for German, "FR" for French).
                              See DeepL documentation for supported languages.

    Returns:
        The translated text, or None if an error occurs.
    """
    try:
        translator = ClientFactory.get_deepl_translator()
        result = translator.translate_text(text, target_lang=target_language_code)
        return result.text
    except Exception as e:
        print(f"Error during translation with DeepL: {e}")
        return None

# Example usage requires a DeepL API key.
# if __name__ == "__main__":
#     if os.environ.get("DEEPL_AUTH_KEY"):
#         note = "High CPU utilization detected on the primary database server."
#         target_lang = "ES"  # Spanish
#
#         translated_note = translate_dashboard_note(note, target_language_code=target_lang)
#
#         if translated_note:
#             print(f"Original ({'en'}): {note}")
#             print(f"Translated ({target_lang}): {translated_note}")
#         else:
#             print("Translation failed.")
#     else:
#         print("DEEPL_AUTH_KEY environment variable not set.")
