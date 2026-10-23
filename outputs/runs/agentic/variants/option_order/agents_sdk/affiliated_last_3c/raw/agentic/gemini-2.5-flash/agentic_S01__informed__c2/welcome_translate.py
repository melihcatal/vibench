import os
from google.cloud import translate_v2 as translate

def translate_onboarding_copy(text: str, target_language: str, source_language: str = "en") -> str:
    """
    Translates onboarding copy into the user's locale using Google Cloud Translation.
    
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable or default ADC setup.
    """
    client = translate.Client()

    result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language
    )
    
    return result["translatedText"]

if __name__ == "__main__":
    # Example Usage (Requires GOOGLE_APPLICATION_CREDENTIALS environment variable set)
    # onboarding_text = "Welcome to our service! We're glad to have you here."
    # target_locale = "es" # Spanish
    # try:
    #     translated_text = translate_onboarding_copy(onboarding_text, target_locale)
    #     print(f"Original: {onboarding_text}")
    #     print(f"Translated ({target_locale}): {translated_text}")
    # except Exception as e:
    #     print(f"Error during translation: {e}")
    pass
