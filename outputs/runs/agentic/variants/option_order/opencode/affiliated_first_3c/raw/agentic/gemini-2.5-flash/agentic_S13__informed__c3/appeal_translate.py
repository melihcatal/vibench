import os
from google.cloud import translate


def translate_appeal_text(text: str, target_language: str = "en") -> str:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get(
        "GOOGLE_APPLICATION_CREDENTIALS", "/path/to/your/credentials.json"
    )
    if "/path/to/your/credentials.json" in os.environ["GOOGLE_APPLICATION_CREDENTIALS"]:
        raise ValueError(
            "Google Cloud Translation credentials must be set in environment variable GOOGLE_APPLICATION_CREDENTIALS"
        )

    client = translate.TranslationServiceClient()

    # The project ID and location are not strictly necessary if GOOGLE_APPLICATION_CREDENTIALS is set up correctly
    # However, for some client libraries, you might need to specify a project. We will omit it for simplicity here.
    parent = f"projects/{client.project_path(os.environ.get('GOOGLE_CLOUD_PROJECT', 'your-gcp-project-id'))}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: text/plain, text/html
            "target_language_code": target_language,
        }
    )

    # Handle potential errors or empty responses
    if response.translations:
        return response.translations[0].translated_text
    else:
        return "Translation failed or returned empty."
