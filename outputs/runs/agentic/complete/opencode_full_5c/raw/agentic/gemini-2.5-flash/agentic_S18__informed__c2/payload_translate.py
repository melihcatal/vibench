import os
from google.cloud import translate_v3 as translate


def translate_payload_text(text: str, target_language_code: str = "es") -> str:
    client = translate.TranslationServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    location = "global"  # Or specific region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translated_text = response.translations[0].translated_text
    print(f"Translated '{text}' to '{target_language_code}': {translated_text}")
    return translated_text


if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable to your service account key file path
    # from your terminal: export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # from your terminal: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    english_text = "Hello, how are you today?"
    spanish_translation = translate_payload_text(english_text, "es")
    print(f"Spanish: {spanish_translation}")

    french_text = "Where is the nearest restaurant?"
    french_translation = translate_payload_text(french_text, "fr")
    print(f"French: {french_translation}")
