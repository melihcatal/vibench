import os
from google.cloud import translate_v2 as translate

def translate_onboarding_copy(text: str, target_language: str = 'es') -> dict:
    """
    Translates onboarding copy into the user's locale using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    translate_client = translate.Client()

    try:
        result = translate_client.translate(
            text,
            target_language=target_language
        )
        return {
            "original_text": text,
            "translated_text": result["translatedText"],
            "source_language": result["detectedSourceLanguage"],
            "target_language": target_language
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # result = translate_onboarding_copy("Welcome to our service! We are happy to have you.", "fr")
    # print(result)
    pass
