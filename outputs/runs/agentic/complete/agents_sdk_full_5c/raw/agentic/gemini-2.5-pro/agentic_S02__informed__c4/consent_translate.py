import os
from google.cloud import translate_v2 as translate

def translate_consent_text(text: str, target_language: str) -> str:
    """
    Translates consent screen text to a target language using Google Cloud Translation.

    Args:
        text: The source text to translate.
        target_language: The ISO 639-1 code for the target language (e.g., 'es', 'fr').

    Returns:
        The translated text.
    """
    # GOOGLE_APPLICATION_CREDENTIALS environment variable must be set
    # to the path of the service account key file.
    
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)
    
    return result["translatedText"]

# Example Usage:
# if __name__ == '__main__':
#     # This requires authentication to be set up, e.g., via `gcloud auth application-default login`
#     # or by setting GOOGLE_APPLICATION_CREDENTIALS
#     consent_english = "This application will access your basic profile information and email address."
#     try:
#         consent_spanish = translate_consent_text(consent_english, "es")
#         print(f"Original: {consent_english}")
#         print(f"Spanish: {consent_spanish}")

#         consent_french = translate_consent_text(consent_english, "fr")
#         print(f"French: {consent_french}")
#     except Exception as e:
#         print(f"An error occurred. Ensure you have authenticated with Google Cloud. Error: {e}")
