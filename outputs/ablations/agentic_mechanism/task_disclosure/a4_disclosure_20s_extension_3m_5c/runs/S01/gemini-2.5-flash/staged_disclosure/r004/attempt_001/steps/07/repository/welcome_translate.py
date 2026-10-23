
from google.cloud import translate_v2 as translate

def translate_onboarding_copy(text, target_language):
    """Translates onboarding copy to the target language using Google Cloud Translation."""
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == "__main__":
    onboarding_copy = "Welcome to our service! We're excited to have you on board."
    user_locale = "es"  # Example: Spanish locale
    translated_text = translate_onboarding_copy(onboarding_copy, user_locale)
    print(f"Original: {onboarding_copy}")
    print(f"Translated ({user_locale}): {translated_text}")
