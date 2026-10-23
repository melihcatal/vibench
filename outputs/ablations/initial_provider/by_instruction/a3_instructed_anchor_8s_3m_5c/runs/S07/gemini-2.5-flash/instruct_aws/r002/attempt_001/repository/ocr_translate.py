from document_client import get_translate_client
from document_models import TranslatedText

def translate_text(text: str, source_language_code: str, target_language_code: str) -> TranslatedText:
    translate_client = get_translate_client()
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )
    return TranslatedText(
        translated_text=response['TranslatedText'],
        source_language=response['SourceLanguageCode'],
        target_language=response['TargetLanguageCode']
    )
