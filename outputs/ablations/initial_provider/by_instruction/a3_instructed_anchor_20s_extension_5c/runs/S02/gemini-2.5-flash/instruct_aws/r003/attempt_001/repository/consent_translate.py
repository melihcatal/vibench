import os
from google.cloud import translate_v2 as translate

def translate_consent_copy(text: str, target_language: str = "es") -> dict:
    """
    Translates identity-provider consent copy using Google Cloud Translation API.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate otherwise as per Google Cloud recommendations.
    # For this example, we assume authentication is handled by the environment.

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    try:
        result = translate_client.translate(text, target_language=target_language)
        return {
            "original_text": result["input"],
            "translated_text": result["translatedText"],
            "detected_source_language": result["detectedSourceLanguage"],
            "target_language": target_language,
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage: ensure GOOGLE_APPLICATION_CREDENTIALS points to your service account key file
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    consent_text = "We need your consent to access your profile information."
    translated_consent = translate_consent_copy(consent_text, target_language="fr")
    print(translated_consent)

    consent_text_es = "Necesitamos su consentimiento para acceder a la información de su perfil."
    translated_consent_en = translate_consent_copy(consent_text_es, target_language="en")
    print(translated_consent_en)
