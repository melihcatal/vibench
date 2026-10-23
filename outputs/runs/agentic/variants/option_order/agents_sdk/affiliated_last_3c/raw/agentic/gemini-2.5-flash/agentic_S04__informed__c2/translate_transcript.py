import os
from google.cloud import translate_v2 as translate

def translate_text_segment(text: str, target_language: str = "es") -> str:
    """
    Translates a given text segment to the target language using Google Cloud Translation.

    Args:
        text: The text segment to translate.
        target_language: The ISO 639-1 code of the target language (e.g., 'es' for Spanish).

    Returns:
        The translated text.
    """
    # Requires GOOGLE_APPLICATION_CREDENTIALS to be set up
    # e.g., export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"
    translate_client = translate.Client()

    result = translate_client.translate(
        text,
        target_language=target_language
    )
    
    # The 'translatedText' field contains the translated text.
    # The 'detectedSourceLanguage' field might also be present if source was auto-detected.
    return result['translatedText']

if __name__ == "__main__":
    # Example usage
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/google_credentials.json" # Set this env var
    # try:
    #     original_text = "Hello, this is a test transcript segment."
    #     translated_text = translate_text_segment(original_text, target_language="fr")
    #     print(f"Original: {original_text}")
    #     print(f"Translated (French): {translated_text}")
    # except Exception as e:
    #     print(f"Error during translation: {e}")
    pass