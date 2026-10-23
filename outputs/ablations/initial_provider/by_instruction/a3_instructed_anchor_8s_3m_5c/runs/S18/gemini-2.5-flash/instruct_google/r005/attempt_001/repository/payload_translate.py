from google.cloud import translate_v3 as translate
import os

def translate_payload_text(text: str, target_language_code: str, project_id: str) -> str:
    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
            "target_language_code": target_language_code,
        }
    )

    translated_text = response.translations[0].translated_text
    return translated_text


if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-google-cloud-project-id")
    example_text = "Hello, world!"
    target_language = "es"
    translated_text = translate_payload_text(example_text, target_language, project_id)
    print(f"Original: {example_text}, Translated ({target_language}): {translated_text}")

    example_text_fr = "Bonjour le monde!"
    target_language_en = "en"
    translated_text_en = translate_payload_text(example_text_fr, target_language_en, project_id)
    print(f"Original: {example_text_fr}, Translated ({target_language_en}): {translated_text_en}")
