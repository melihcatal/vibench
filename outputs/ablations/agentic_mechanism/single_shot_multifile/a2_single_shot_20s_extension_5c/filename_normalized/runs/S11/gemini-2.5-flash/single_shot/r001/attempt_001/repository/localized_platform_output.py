from model_models import TranslationRequest, TranslationResponse
from model_client import get_google_cloud_translate_client, get_vertex_ai_project_location
from google.cloud import translate_v3

def translate_with_google_cloud(request: TranslationRequest) -> TranslationResponse:
    client = get_google_cloud_translate_client()
    project_id, _ = get_vertex_ai_project_location()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"
    try:
        response = client.translate_text(
            parent=parent,
            contents=[request.text],
            target_language_code=request.target_language_code,
        )
        translated_text = response.translations[0].translated_text if response.translations else ""
        return TranslationResponse(translated_text=translated_text)
    except translate_v3.exceptions.GoogleAPIError as e: raise RuntimeError(f"Google Cloud Translation API error: {e}")