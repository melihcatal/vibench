from google.cloud import translate_v2 as translate
from identity_client import get_identity_config


def translate_consent_text(text: str, target_language: str) -> str:
    config = get_identity_config()
    # Note: Google Cloud Translate library uses ADC (Application Default Credentials)
    # or you can explicitly pass credentials. For simplicity, we assume ADC is set up.
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/credentials.json'

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]


if __name__ == "__main__":
    # This is not example usage, but for verification.
    # In a real application, this would translate consent screens for users.

    consent_text_en = (
        "This application will access your profile information and email address."
    )
    target_lang = "es"  # Spanish

    try:
        translated_text = translate_consent_text(consent_text_en, target_lang)
        print(f"Original (en): {consent_text_en}")
        print(f"Translated ({target_lang}): {translated_text}")
    except Exception as e:
        print(f"Failed to translate text: {e}")
        print(
            "Please ensure Google Cloud ADC is configured or GOOGLE_APPLICATION_CREDENTIALS is set."
        )
