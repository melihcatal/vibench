from google.cloud import translate_v3 as translate
from typing import Generator
from speech_models import SpeechRecognitionResult # Assuming SpeechRecognitionResult is generic enough

def live_caption_translate(caption_results: Generator[SpeechRecognitionResult, None, None], target_language: str, project_id: str) -> Generator[str, None, None]:
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}"

    for result in caption_results:
        if result.is_final and result.text:
            response = client.translate_text(
                request={
                    "parent": parent,
                    "contents": [result.text],
                    "target_language_code": target_language,
                }
            )
            for translation in response.translations:
                yield translation.translated_text
