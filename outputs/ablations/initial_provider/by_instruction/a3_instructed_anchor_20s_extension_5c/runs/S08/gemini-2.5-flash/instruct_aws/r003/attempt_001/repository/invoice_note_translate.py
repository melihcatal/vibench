from google.cloud import translate_v2 as translate
import os

def translate_invoice_notes(text_content: str, target_language: str = 'en') -> dict:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation API.
    """
    # Instantiates a client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS points to your service account key file
    # or use GOOGLE_API_KEY if not running in Google Cloud environment
    translate_client = translate.Client()

    try:
        response = translate_client.translate(text_content, target_language=target_language)
        return {
            "original_text": text_content,
            "translated_text": response['translatedText'],
            "detected_source_language": response['detectedSourceLanguage']
        }
    except Exception as e:
        return {"error": f"Error translating text with Google Cloud Translation API: {e}"}
