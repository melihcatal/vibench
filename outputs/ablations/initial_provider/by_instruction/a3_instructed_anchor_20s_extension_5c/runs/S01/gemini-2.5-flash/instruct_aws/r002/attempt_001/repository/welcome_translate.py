from identity_client import AWSClient
from identity_models import TranslateRequest, TranslateResponse

def welcome_translate(request: TranslateRequest) -> TranslateResponse:
    aws_client = AWSClient()
    translate_client = aws_client.get_translate_client()

    try:
        response = translate_client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_language_code,
            TargetLanguageCode=request.target_language_code
        )
        return TranslateResponse(translated_text=response['TranslatedText'])
    except Exception as e:
        return TranslateResponse(translated_text=f"Translation failed: {str(e)}")
