import boto3
from storage_client import get_translate_client
from storage_models import TranslateTextRequest, TranslateTextResponse

def translate_text_from_stored_document(request: TranslateTextRequest) -> TranslateTextResponse:
    """
    Translates text extracted from a stored document using AWS Translate.
    """
    translate_client = get_translate_client()
    try:
        response = translate_client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_language_code,
            TargetLanguageCode=request.target_language_code
        )
        translated_text = response['TranslatedText']
        return TranslateTextResponse(success=True, translated_text=translated_text, message="Text translated successfully.")
    except translate_client.exceptions.UnsupportedLanguagePairException as e:
        return TranslateTextResponse(success=False, message=f"Unsupported language pair: {e}")
    except translate_client.exceptions.TextSizeLimitExceededException as e:
        return TranslateTextResponse(success=False, message=f"Text size limit exceeded: {e}")
    except Exception as e:
        return TranslateTextResponse(success=False, message=f"Error translating text: {e}")

