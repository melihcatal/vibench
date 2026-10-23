from typing import Generator, Dict, Any
from google.cloud import translate_v2 as translate

from speech_models import SpeechRecognitionResult

def live_caption_translate(event_stream: Generator[SpeechRecognitionResult, None, None], target_language: str = "es") -> Generator[Dict[str, Any], None, None]:
    translate_client = translate.Client()

    for result in event_stream:
        if result.is_final and result.text:
            translation = translate_client.translate(result.text, target_language=target_language)
            yield {
                "original_text": result.text,
                "translated_text": translation['translatedText'],
                "target_language": target_language,
                "detected_source_language": translation['detectedSourceLanguage']
            }
