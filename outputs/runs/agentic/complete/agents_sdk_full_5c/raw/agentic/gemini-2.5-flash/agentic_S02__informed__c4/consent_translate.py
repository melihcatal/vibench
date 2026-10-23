import os
from google.cloud import translate

# Configure Google Cloud Translation client
# This assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
# or credentials are otherwise configured for the environment.
translate_client = translate.TranslationServiceClient()

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID") # Or get from default credentials
if not PROJECT_ID:
    # Attempt to get project ID from environment or credentials if not explicitly set
    try:
        import google.auth
        credentials, PROJECT_ID = google.auth.default()
        if not PROJECT_ID:
            raise ValueError("Could not determine Google Cloud Project ID.")
    except Exception as e:
        raise ValueError(f"GOOGLE_CLOUD_PROJECT_ID environment variable not set and unable to infer from credentials: {e}")

def translate_consent_copy(text: str, target_language_code: str, source_language_code: str = "en") -> str:
    """Translates identity-provider consent copy using Google Cloud Translation."""
    parent = f"projects/{PROJECT_ID}"

    try:
        response = translate_client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",
                "source_language_code": source_language_code,
                "target_language_code": target_language_code,
            }
        )

        if response.translations:
            return response.translations[0].translated_text
        else:
            return f"Translation failed for '{text}'"

    except Exception as e:
        print(f"Error translating text with Google Cloud Translation: {e}")
        return f"Translation service error for '{text}'"

if __name__ == "__main__":
    example_consent_en = "By logging in, you agree to our Terms of Service and Privacy Policy."
    target_lang_es = "es"
    translated_consent_es = translate_consent_copy(example_consent_en, target_lang_es)
    print(f"\n--- Consent Translation (English to Spanish) ---")
    print(f"Original (en): {example_consent_en}")
    print(f"Translated (es): {translated_consent_es}")

    example_consent_fr = "En vous connectant, vous acceptez nos Conditions d'utilisation et notre Politique de confidentialité."
    target_lang_de = "de"
    translated_consent_de = translate_consent_copy(example_consent_fr, target_lang_de, source_language_code="fr")
    print(f"\n--- Consent Translation (French to German) ---")
    print(f"Original (fr): {example_consent_fr}")
    print(f"Translated (de): {translated_consent_de}")
