from typing import Dict

from google.cloud import translate_v3 as translate

from speech_models import normalize_stream_event


class LiveCaptionTranslator:
    def __init__(self, project_id: str, target_language: str) -> None:
        self.client = translate.TranslationServiceClient()
        self.parent = f'projects/{project_id}/locations/global'
        self.target_language = target_language

    def translate_caption(self, caption_event: Dict[str, object]) -> Dict[str, object]:
        event = normalize_stream_event(
            transcript=str(caption_event.get('transcript', '')),
            is_final=bool(caption_event.get('is_final', False)),
            confidence=caption_event.get('confidence'),
            language_code=str(caption_event.get('language_code', 'en-US')),
        )
        response = self.client.translate_text(
            request={
                'parent': self.parent,
                'contents': [event['transcript']],
                'mime_type': 'text/plain',
                'target_language_code': self.target_language,
            }
        )
        translated = response.translations[0].translated_text if response.translations else ''
        return {
            **event,
            'translated_text': translated,
            'target_language': self.target_language,
        }

