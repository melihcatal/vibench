from speech_client import SpeechClient
from speech_models import TranslateRequest


def translate_transcript(request: TranslateRequest, config=None) -> dict:
    config = config or {}
    client = SpeechClient(region_name=config.get("region")).get_translate_client()

    response = client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_language_code,
        TargetLanguageCode=request.target_language_code,
    )

    return {
        "translated_text": response["TranslatedText"],
        "source_language_code": response["SourceLanguageCode"],
        "target_language_code": response["TargetLanguageCode"],
    }
