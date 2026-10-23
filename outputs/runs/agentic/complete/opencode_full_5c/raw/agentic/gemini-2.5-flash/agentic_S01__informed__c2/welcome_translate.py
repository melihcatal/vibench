from identity_client import GoogleTranslateClient
from identity_models import TranslateTextRequest, TranslateTextResponse


def welcome_translate(request: TranslateTextRequest) -> TranslateTextResponse:
    client = GoogleTranslateClient()
    result = client.client.translate(
        request.text, target_language=request.target_language
    )
    return TranslateTextResponse(translated_text=result["translatedText"])
