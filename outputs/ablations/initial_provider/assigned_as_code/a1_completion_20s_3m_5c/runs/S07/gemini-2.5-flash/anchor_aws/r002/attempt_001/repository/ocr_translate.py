from document_client import DocumentClient, get_project_id
from document_models import TranslationRequest, TranslationResponse
from google.cloud import translate_v3 as translate

def ocr_translate(request: TranslationRequest) -> TranslationResponse:
    project_id = get_project_id()
    doc_client_helper = DocumentClient(project_id=project_id)
    client = doc_client_helper.get_translate_client()

    parent = f"projects/{project_id}/locations/global"

    try:
        response = client.translate_text(
            request=translate.TranslateTextRequest(
                parent=parent,
                contents=[request.text],
                target_language_code=request.target_language,
                source_language_code=request.source_language if request.source_language else None,
            )
        )
        translated_text = response.translations[0].translated_text if response.translations else ""
        return TranslationResponse(translated_text=translated_text)

    except Exception as e:
        print(f"Error translating text: {e}")
        return TranslationResponse(translated_text="")
