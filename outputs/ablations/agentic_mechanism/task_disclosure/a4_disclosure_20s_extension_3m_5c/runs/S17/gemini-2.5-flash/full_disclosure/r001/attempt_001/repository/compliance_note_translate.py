
from google.cloud import translate_v2 as translate

def translate_compliance_note(text: str, target_language: str = "en") -> str:
    """
    Translates encryption or compliance notes for reviewers using Google Cloud Translation.

    Args:
        text: The text of the note to translate.
        target_language: The language to translate the text into (e.g., "en" for English, "es" for Spanish).

    Returns:
        The translated text.
    """
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication
    # e.g., export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    note_to_translate = "Diese Notiz enthält wichtige Informationen zur Verschlüsselung."
    translated_note = translate_compliance_note(note_to_translate, "en")
    print(f"Original: {note_to_translate}")
    print(f"Translated: {translated_note}")

    note_to_translate_es = "This note contains important encryption information."
    translated_note_es = translate_compliance_note(note_to_translate_es, "es")
    print(f"Original: {note_to_translate_es}")
    print(f"Translated: {translated_note_es}")
