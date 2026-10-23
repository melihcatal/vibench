from google.cloud import translate_v3 as translate
import os

def translate_payload_text(project_id: str, text: str, target_language_code: str = "es") -> str:
    """Translates customer-facing message payload text using Google Cloud Translation API."""
    client = translate.TranslationServiceClient()
    location = "global"  # Or specific region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    if response.translations:
        translated_text = response.translations[0].translated_text
        print(f"Original: '{text}'")
        print(f"Translated to {target_language_code}: '{translated_text}'")
        return translated_text
    return text # Return original text if no translation found

if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    
    english_text = "Thank you for your order! Your package will arrive in 3-5 business days."
    spanish_translation = translate_payload_text(PROJECT_ID, english_text, "es")
    print(f"Spanish: {spanish_translation}")

    french_text = "Welcome to our new service."
    french_translation = translate_payload_text(PROJECT_ID, french_text, "fr")
    print(f"French: {french_translation}")
