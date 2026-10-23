from google.cloud import translate_v3 as translate
from storage_models import TranslationRequest

def translate_text_content(request: TranslationRequest, project_id: str) -> str:
    """Translates text using Google Cloud Translation.

    Args:
        request: A TranslationRequest object.
        project_id: Your Google Cloud project ID.

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text_content],
            "target_language_code": request.target_language,
            "source_language_code": request.source_language,
        }
    )

    translated_text = response.translations[0].translated_text
    print(f"Translated text from '{request.source_language or "auto"}' to '{request.target_language}': {translated_text}")
    return translated_text

if __name__ == '__main__':
    # Example usage (replace with actual values)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up and Cloud Translation API is enabled.
    # project_id = "your-gcp-project-id"
    # text_to_translate = "Hello, how are you?"
    # translate_req = TranslationRequest(text_content=text_to_translate, target_language="es", source_language="en")
    # translated = translate_text_content(translate_req, project_id)
    # print(f"Original: {text_to_translate}, Translated: {translated}")

    # translate_req_auto = TranslationRequest(text_content="Bonjour le monde", target_language="en")
    # translated_auto = translate_text_content(translate_req_auto, project_id)
    # print(f"Original: Bonjour le monde, Translated: {translated_auto}")
    pass
