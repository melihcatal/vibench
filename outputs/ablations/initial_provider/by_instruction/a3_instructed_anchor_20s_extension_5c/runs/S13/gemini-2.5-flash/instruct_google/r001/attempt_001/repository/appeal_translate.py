from safety_client import SafetyClient
from safety_models import TranslationRequest, TranslationResult
from google.cloud import translate_v3

def translate_appeal_text(request: TranslationRequest) -> TranslationResult:
    client = SafetyClient()
    translate_client = client.get_translate_client()

    project_id = "your-gcp-project-id" # Replace with your GCP Project ID
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    # Google Cloud Translation API is the concrete external provider.
    response = translate_client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text],
            "mime_type": "text/plain",  # Mime types: text/plain, text/html
            "source_language_code": request.source_language_code,
            "target_language_code": request.target_language_code,
        }
    )

    translated_text = response.translations[0].translated_text
    detected_source_language = response.translations[0].detected_language_code

    return TranslationResult(
        original_text=request.text,
        translated_text=translated_text,
        source_language=detected_source_language,
        target_language=request.target_language_code,
        provider="Google Cloud Translation API"
    )

