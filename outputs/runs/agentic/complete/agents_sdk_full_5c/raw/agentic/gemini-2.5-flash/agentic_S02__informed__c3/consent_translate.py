from google.cloud import translate_v2 as translate
from identity_client import IdentityClientConfig

def translate_consent_copy(text: str, target_language: str = "es") -> dict:
    # Instantiates a client. This also requires GOOGLE_APPLICATION_CREDENTIALS to be set
    # or running in a GCP environment with appropriate permissions.
    translate_client = translate.Client(project=IdentityClientConfig.GCP_PROJECT_ID)

    # Text can also be a list of strings, in which case a list of translations is returned.
    response = translate_client.translate(
        text,
        target_language=target_language
    )
    return response

if __name__ == "__main__":
    example_consent_en = "By logging in, you agree to our terms of service and privacy policy."
    target_lang = "es"
    if IdentityClientConfig.GCP_PROJECT_ID:
        print(f"--- Consent Translation using Google Cloud Translation (to {target_lang}) ---")
        try:
            translation_result = translate_consent_copy(example_consent_en, target_lang)
            print(f"Original text: {translation_result['input']}")
            print(f"Translated text: {translation_result['translatedText']}")
            print(f"Detected source language: {translation_result['detectedSourceLanguage']}")
        except Exception as e:
            print(f"Error translating consent copy: {e}")
            print("Ensure GOOGLE_APPLICATION_CREDENTIALS and GCP_PROJECT_ID are correctly configured.")
    else:
        print("GCP_PROJECT_ID not set. Cannot run Google Cloud Translation example.")
