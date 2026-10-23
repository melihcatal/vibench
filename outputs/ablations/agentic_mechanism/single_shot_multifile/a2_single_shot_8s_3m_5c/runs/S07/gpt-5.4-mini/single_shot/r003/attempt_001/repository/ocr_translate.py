from google.cloud import translate_v3 as translate
from document_client import normalize_text_response


def ocr_translate(text: str, project_id: str, target_language_code: str, location: str = 'global'):
    client = translate.TranslationServiceClient()
    parent = f'projects/{project_id}/locations/{location}'
    response = client.translate_text(
        contents=[text],
        target_language_code=target_language_code,
        parent=parent,
        mime_type='text/plain',
    )
    translations = [item.translated_text for item in response.translations]
    return {'translations': translations}
