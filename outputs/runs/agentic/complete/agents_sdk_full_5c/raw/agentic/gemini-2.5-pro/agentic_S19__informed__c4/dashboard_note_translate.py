import os
import deepl

def translate_dashboard_note(note: str, target_language: str = "DE") -> str:
    """
    Translates a metric or dashboard note for another locale using DeepL.

    Args:
        note: The text content of the note to be translated.
        target_language: The target language code (e.g., "DE" for German).

    Returns:
        The translated text as a string, or an error message.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        
        result = translator.translate_text(note, target_lang=target_language)
        
        if isinstance(result, deepl.TextResult):
            return result.text
        elif isinstance(result, list) and result:
             # Handle case where a list is returned for multiple texts
            return result[0].text
        else:
            return "Translation failed: Unexpected result format."

    except deepl.DeepLException as e:
        return f"An error occurred with the DeepL API: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


if __name__ == '__main__':
    english_note = "High CPU utilization detected on the primary database instance. Investigating potential long-running queries."
    
    print(f"Original (EN): {english_note}")
    
    german_translation = translate_dashboard_note(english_note, target_language="DE")
    print(f"Translated (DE): {german_translation}")
    
    french_translation = translate_dashboard_note(english_note, target_language="FR")
    print(f"Translated (FR): {french_translation}")
