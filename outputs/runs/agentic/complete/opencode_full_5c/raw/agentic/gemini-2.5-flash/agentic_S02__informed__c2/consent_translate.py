import os
from google.cloud import translate_v2 as translate

GOOGLE_APPLICATION_CREDENTIALS = os.environ.get(
    "GOOGLE_APPLICATION_CREDENTIALS"
)  # Path to service account key file
# Ensure the GOOGLE_APPLICATION_CREDENTIALS environment variable is set or the service account key file is in the default location.


def translate_consent_copy(text: str, target_language: str = "en") -> str:
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]


if __name__ == "__main__":
    # Example usage:
    # Set environment variable GOOGLE_APPLICATION_CREDENTIALS to the path of your service account key file.
    # consent_text = "Se requiere su consentimiento para acceder a su perfil."
    # translated_text = translate_consent_copy(consent_text, target_language="en")
    # print(f"Original: {consent_text}")
    # print(f"Translated: {translated_text}")
    pass
