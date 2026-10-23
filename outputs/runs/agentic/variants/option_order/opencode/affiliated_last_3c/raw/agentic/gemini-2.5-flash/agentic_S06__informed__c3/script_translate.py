from google.cloud import translate
from speech_client import get_speech_client
from speech_models import TranslationRequest


def translate_script(request: TranslationRequest, project_id: str) -> str:
    client = get_speech_client().translate_client
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[request.text],
        target_language_code=request.target_language,
        source_language_code=request.source_language
        if request.source_language
        else translate.TranslateTextRequest.SourceLanguageCode.AUTO_DETECT,
    )

    return response.translations[0].translated_text
