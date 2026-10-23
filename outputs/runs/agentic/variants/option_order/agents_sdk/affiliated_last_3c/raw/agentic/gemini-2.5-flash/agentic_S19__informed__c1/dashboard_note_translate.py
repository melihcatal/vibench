from google.cloud import translate_v2 as translate
import os

def translate_dashboard_note(text: str, target_language: str = "es") -> str:
    """Translates metric or dashboard notes for another locale using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language: The BCP-47 language code of the target language (e.g., 'es' for Spanish).

    Returns:
        The translated text.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up
    translate_client = translate.Client()

    try:
        result = translate_client.translate(
            text,
            target_language=target_language
        )
        return result['translatedText']
    except Exception as e:
        return f"Error during translation: {e}"

if __name__ == "__main__":
    # Example usage
    dashboard_note_en = "The CPU utilization is currently at critical levels due to an unexpected traffic surge."
    target_lang = "fr"

    print(f"Translating dashboard note to {target_lang}...")
    translated_note = translate_dashboard_note(dashboard_note_en, target_language=target_lang)
    print("\n--- Original Note ---")
    print(dashboard_note_en)
    print("\n--- Translated Note ---")
    print(translated_note)
    print("-----------------------")
