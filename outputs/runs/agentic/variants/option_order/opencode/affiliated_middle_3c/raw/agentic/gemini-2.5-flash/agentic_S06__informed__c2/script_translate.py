from speech_client import get_translation_client
from speech_models import TranslateTextRequest, TranslateTextResponse
from google.cloud import translate_v3 as translate


def script_translate(request: TranslateTextRequest) -> TranslateTextResponse:
    client = get_translation_client()

    parent = f"projects/{client.project}"

    response = client.translate_text(
        parent=parent,
        contents=[request.text],
        target_language_code=request.target_language_code,
        source_language_code=request.source_language_code,
    )

    # The API returns a list of translations, we only sent one text, so take the first.
    translated_text = response.translations[0].translated_text
    return TranslateTextResponse(translated_text=translated_text)
