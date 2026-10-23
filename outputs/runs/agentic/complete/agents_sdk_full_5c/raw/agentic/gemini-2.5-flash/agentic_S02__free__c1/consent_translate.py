from google.cloud import translate_v3 as translate
from typing import List

from identity_client import GCP_PROJECT_ID, GCP_REGION

def translate_consent_copy(
    text_to_translate: List[str],
    target_language_code: str,
    source_language_code: str = "en",
) -> List[str]:
    """
    Translates identity provider consent copy using Google Cloud Translation API.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{GCP_PROJECT_ID}/locations/{GCP_REGION}"

    translated_texts = []

    for text in text_to_translate:
        response = client.translate_text(
            parent=parent,
            contents=[text],
            mime_type="text/plain",  # Set to "text/html" if translating HTML.
            source_language_code=source_language_code,
            target_language_code=target_language_code,
        )

        for translation in response.translations:
            translated_texts.append(translation.translated_text)
    
    print(f"Successfully translated {len(text_to_translate)} consent strings to {target_language_code}.")
    return translated_texts

if __name__ == "__main__":
    consent_strings = [
        "By clicking 'Accept', you agree to our Terms of Service and Privacy Policy.",
        "We need your consent to access your profile information.",
        "Please review the permissions requested by this application."
    ]
    target_lang = "es" # Spanish

    print(f"Translating consent strings to {target_lang}...")
    try:
        translated_strings = translate_consent_copy(consent_strings, target_lang)
        for original, translated in zip(consent_strings, translated_strings):
            print(f"Original ({'en'}): {original}")
            print(f"Translated ({target_lang}): {translated}\n")
    except Exception as e:
        print(f"Error during translation: {e}")
        print("Please ensure your GCP_PROJECT_ID and GCP_REGION are correct.")
        print("Also, ensure you have appropriate IAM permissions for the Cloud Translation API.")
