
from google.cloud import translate_v2 as translate

def translate_onboarding_copy(text, target_locale):
    """Translates onboarding copy into the target locale using Google Cloud Translation."""
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_locale)
    return result['translatedText']

if __name__ == "__main__":
    onboarding_text = "Welcome to our service! We are happy to have you."
    user_locale = "es"  # Example: Spanish

    translated_text = translate_onboarding_copy(onboarding_text, user_locale)
    print(f"Original English: {onboarding_text}")
    print(f"Translated ({user_locale}): {translated_text}")
