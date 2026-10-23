from translation_client import get_translation_client
from translation_models import DictionaryTranslationRequest

def translate_dictionary_values(request: DictionaryTranslationRequest) -> dict[str, str]:
    client = get_translation_client()
    parent = f"projects/{request.project_id}/locations/global"

    translated_dict = {}
    for key, value in request.data.items():
        response = client.translate_text(
            parent=parent,
            contents=[value],
            target_language_code=request.target_language,
            source_language_code=request.source_language,
            mime_type='text/plain'
        )
        translated_dict[key] = response.translations[0].translated_text

    return translated_dict
