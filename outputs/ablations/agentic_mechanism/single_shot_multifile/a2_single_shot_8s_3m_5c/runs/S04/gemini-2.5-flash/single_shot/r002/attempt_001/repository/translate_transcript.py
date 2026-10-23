from speech_client import get_aws_translate_client
from speech_models import TranslatedSegment

def translate_transcript_segment(text: str, source_language: str, target_language: str) -> TranslatedSegment:
    translate_client = get_aws_translate_client()

    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )

    return TranslatedSegment(
        original_text=text,
        translated_text=response["TranslatedText"],
        source_language=source_language,
        target_language=target_language
    )
