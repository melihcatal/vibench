from typing import Dict, List, Optional

from speech_models import normalize_stream_event


class PartialResultAggregator:
    def __init__(self) -> None:
        self.partial: str = ''
        self.final_transcripts: List[str] = []

    def handle_event(self, event: Dict[str, object]) -> Dict[str, object]:
        normalized = normalize_stream_event(
            transcript=str(event.get('transcript', '')),
            is_final=bool(event.get('is_final', False)),
            confidence=event.get('confidence'),
            language_code=str(event.get('language_code', 'en-US')),
        )
        if normalized['is_final']:
            self.final_transcripts.append(normalized['transcript'])
            self.partial = ''
        else:
            self.partial = normalized['transcript']
        return normalized

    def snapshot(self) -> Dict[str, object]:
        return {
            'partial': self.partial,
            'final_transcripts': list(self.final_transcripts),
        }

