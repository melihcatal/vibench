from vision_client import VisionClient
from vision_models import AltTextTranslateRequest, AltTextTranslateResponse
import os

def alt_text_translate(request: AltTextTranslateRequest) -> AltTextTranslateResponse:
    client = VisionClient(region_name=os.environ.get('AWS_REGION', 'us-east-1')).translate_client
    response = client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_language,
        TargetLanguageCode=request.target_language
    )
    translated_text = response.get('TranslatedText', '')
    return AltTextTranslateResponse(translated_text=translated_text)
