"""
Translates encryption or compliance notes for reviewers using Google Cloud Translation API.
"""
import os
from google.cloud import translate_v2 as translate

def translate_note(text: str, target_language: str) -> str:
    """
    Translates a given text into the target language using Google Cloud Translation.

    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set
    for a service account with Translation API access.

    Args:
        text: The text string to translate.
        target_language: The ISO 639-1 code for the target language (e.g., 'es', 'fr', 'ja').

    Returns:
        The translated text string.
    """
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        raise EnvironmentError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is not set. "
            "Please point it to your GCP service account JSON key file."
        )

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)
    
    return result["translatedText"]

# Example Usage (for demonstration if run directly)
if __name__ == '__main__':
    compliance_note_en = (
        "All data at rest must be encrypted using AES-256. "
        "Key rotation policy is set to 90 days. "
        "Access is restricted to authorized personnel via IAM roles."
    )
    
    target_lang = 'es' # Spanish

    if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print(f"Original note (en):\n{compliance_note_en}\n")
        print(f"Translating to '{target_lang}'...")
        
        translated_text = translate_note(compliance_note_en, target_lang)
        
        print(f"\nTranslated note ({target_lang}):\n{translated_text}")
    else:
        print("Skipping example: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
