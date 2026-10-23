import os
from google.cloud import translate_v2 as translate

# Google Cloud Translation specific environment variables
# GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT")

def translate_appeal_text(text: str, target_language: str = "en") -> str:
    """
    Translates appeal text for review using Google Cloud Translation API.
    
    Args:
        text: The appeal text to translate.
        target_language: The ISO 639-1 code of the target language (e.g., "en" for English).
    
    Returns:
        The translated text.
    """
    # Initialize Google Cloud Translation client
    # This requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set
    # or gcloud auth application-default login
    translate_client = translate.Client()
    
    try:
        result = translate_client.translate(text, target_language=target_language)
        return result['translatedText']
    except Exception as e:
        print(f"Error translating appeal text with Google Cloud Translation: {e}")
        return text # Return original text on error

if __name__ == '__main__':
    # Example usage (requires Google Cloud authentication)
    # appeal_message_es = "Este es un mensaje de apelación en español."
    # translated_en = translate_appeal_text(appeal_message_es, "en")
    # print(f"Original (ES): {appeal_message_es}")
    # print(f"Translated (EN): {translated_en}")

    # appeal_message_fr = "Je voudrais faire appel de cette décision."
    # translated_en_fr = translate_appeal_text(appeal_message_fr, "en")
    # print(f"Original (FR): {appeal_message_fr}")
    # print(f"Translated (EN): {translated_en_fr}")
    pass
