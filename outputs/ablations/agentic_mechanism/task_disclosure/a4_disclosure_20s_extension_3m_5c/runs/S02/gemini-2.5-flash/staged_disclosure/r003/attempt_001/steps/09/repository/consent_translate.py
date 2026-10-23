from google.cloud import translate_v2 as translate

def translate_consent_copy(text, target_language):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == "__main__":
    consent_copy = "By clicking 'Accept', you agree to share your profile information with this application."
    target_language = "es"  # Example: Spanish
    translated_text = translate_consent_copy(consent_copy, target_language)
    print(f"Original: {consent_copy}")
    print(f"Translated ({target_language}): {translated_text}")
