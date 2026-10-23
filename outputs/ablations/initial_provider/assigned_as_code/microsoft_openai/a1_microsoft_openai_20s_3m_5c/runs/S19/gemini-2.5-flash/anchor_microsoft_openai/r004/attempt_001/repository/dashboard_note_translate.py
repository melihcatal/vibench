from observability_client import GcpObservabilityClient
from google.cloud.translate_v3 import TranslationServiceClient, TranslateTextRequest

def dashboard_note_translate(payload, config=None):
    config = config or {}
    project_id = config.get('gcp_project_id')
    text_to_translate = payload['note_text']
    target_language_code = payload['target_language']
    source_language_code = payload.get('source_language') # Optional, will be auto-detected if not provided

    client = GcpObservabilityClient().translate_client

    parent = f"projects/{project_id}/locations/global" # Translation API typically uses 'global' location

    request_args = {
        "parent": parent,
        "contents": [text_to_translate],
        "target_language_code": target_language_code,
    }
    if source_language_code:
        request_args["source_language_code"] = source_language_code

    request = TranslateTextRequest(**request_args)
    response = client.translate_text(request=request)

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    return {'translated_text': translated_text}
