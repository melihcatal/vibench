import boto3
from storage_client import get_translate_client
from storage_models import TranslatedTextResult

def translate_document_text(text: str, source_language_code: str, target_language_code: str) -> TranslatedTextResult:
    """
    Translates text extracted from a stored document using AWS Translate.
    """
    translate_client = get_translate_client()
    
    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
        return TranslatedTextResult(
            translated_text=response['TranslatedText'],
            source_language_code=response['SourceLanguageCode'],
            target_language_code=response['TargetLanguageCode']
        )
    except translate_client.exceptions.ClientError as e:
        print(f"Error translating text: {e}")
        raise

if __name__ == '__main__':
    # Example usage:
    # text_to_translate = "Hello, how are you?"
    # source_lang = "en"
    # target_lang = "es"
    # try:
    #     translated_result = translate_document_text(text_to_translate, source_lang, target_lang)
    #     print(f"Original: {text_to_translate}")
    #     print(f"Translated ({source_lang} -> {target_lang}): {translated_result.translated_text}")
    # except Exception as e:
    #     print(f"Translation failed: {e}")
    pass
