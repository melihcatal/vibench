import os
from google.cloud import translate_v2 as translate


def translate_invoice_notes(text_to_translate: str, target_language: str = 'en', config=None) -> str:
    config = config or {}
    # Google Cloud Translation client implicitly uses GOOGLE_APPLICATION_CREDENTIALS environment variable
    # or can be configured with a project ID. For simplicity, we assume GOOGLE_APPLICATION_CREDENTIALS is set.
    # If using API Key, it would be passed to the client.

    # For this example, we'll create a client directly. If a project ID is needed for certain setups,
    # it would be passed during client initialization or set as an environment variable.
    # project_id = config.get('GOOGLE_CLOUD_PROJECT_ID', os.environ.get('GOOGLE_CLOUD_PROJECT_ID'))
    # client = translate.Client(project=project_id)

    client = translate.Client()

    if not text_to_translate:
        return ""

    try:
        result = client.translate(text_to_translate, target_language=target_language)
        return result['translatedText']
    except Exception as e:
        return f"Error translating text: {e}"
