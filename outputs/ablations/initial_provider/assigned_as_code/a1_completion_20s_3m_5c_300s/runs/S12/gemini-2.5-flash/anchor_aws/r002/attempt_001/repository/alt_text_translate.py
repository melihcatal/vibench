import boto3
from typing import Dict, Any
from vision_client import get_translate_client
from vision_models import TranslateTextRequest, TranslateTextResponse

def alt_text_translate(payload: TranslateTextRequest, config: Dict[str, Any]) -> TranslateTextResponse:
    client = get_translate_client(config)

    response = client.translate_text(
        Text=payload.text,
        SourceLanguageCode=payload.source_language,
        TargetLanguageCode=payload.target_language
    )

    translated_text = response.get('TranslatedText', '')

    return TranslateTextResponse(translated_text=translated_text)
