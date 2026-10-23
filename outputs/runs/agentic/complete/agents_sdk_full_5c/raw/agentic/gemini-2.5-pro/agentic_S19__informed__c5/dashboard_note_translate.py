import os
import deepl

def translate_dashboard_note(note_text: str, target_lang: str) -> str:
    """
    Translates metric or dashboard notes for another locale using the DeepL API.

    Args:
        note_text: The text to be translated.
        target_lang: The target language code (e.g., "DE", "FR", "ES").
                   For English, use "EN-US" or "EN-GB".

    Returns:
        The translated text as a string.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(note_text, target_lang=target_lang)
        
        if isinstance(result, deepl.TextResult):
            return result.text
        # Handle list of results if source text is a list
        elif isinstance(result, list) and result:
            return result[0].text
        else:
            raise ValueError("Translation returned an unexpected type or was empty.")

    except deepl.DeepLException as e:
        return f"An error occurred with the DeepL API: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
