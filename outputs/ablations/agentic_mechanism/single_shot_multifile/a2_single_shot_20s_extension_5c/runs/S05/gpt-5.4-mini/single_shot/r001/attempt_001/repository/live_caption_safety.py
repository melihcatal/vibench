from typing import Dict

from google.cloud import aiplatform
from google.cloud import language_v1

from speech_models import normalize_stream_event


class LiveCaptionSafetyChecker:
    def __init__(self, project_id: str, location: str = 'us-central1') -> None:
        self.project_id = project_id
        self.location = location
        self.client = language_v1.LanguageServiceClient()

    def check(self, caption_event: Dict[str, object]) -> Dict[str, object]:
        event = normalize_stream_event(
            transcript=str(caption_event.get('transcript', '')),
            is_final=bool(caption_event.get('is_final', False)),
            confidence=caption_event.get('confidence'),
            language_code=str(caption_event.get('language_code', 'en-US')),
        )
        document = language_v1.Document(content=event['transcript'], type_=language_v1.Document.Type.PLAIN_TEXT)
        response = self.client.moderate_text(request={'document': document}) if hasattr(self.client, 'moderate_text') else None
        unsafe = bool(response.moderation_categories) if response is not None and hasattr(response, 'moderation_categories') else False
        return {**event, 'unsafe': unsafe, 'provider': 'google-cloud-language'}

