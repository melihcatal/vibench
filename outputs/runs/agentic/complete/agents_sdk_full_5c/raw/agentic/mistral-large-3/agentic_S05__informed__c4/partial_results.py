from typing import Optional
from dashscope import SpeechRecognizer
from speech_models import TranscriptEvent

class PartialResultHandler:
    def __init__(self):
        self._current_transcript = ""
        self._final_transcripts = []

    def handle(self, result: dict):
        event = TranscriptEvent(
            text=result.get("text", ""),
            is_final=result.get("is_final", False),
            timestamp=result.get("timestamp", 0)
        )
        
        if event.is_final:
            self._final_transcripts.append(event.text)
            self._current_transcript = ""
        else:
            self._current_transcript = event.text
        
        self._print_result(event)

    def _print_result(self, event: TranscriptEvent):
        status = "FINAL" if event.is_final else "PARTIAL"
        print(f"[{status}] {event.text}")

    def get_final_transcripts(self) -> list[str]:
        return self._final_transcripts

    def get_current_transcript(self) -> str:
        return self._current_transcript


def setup_recognizer(handler: PartialResultHandler) -> SpeechRecognizer:
    recognizer = SpeechRecognizer(
        model="paraformer-realtime-v1",
        format="pcm",
        sample_rate=16000,
        callback=handler.handle
    )
    return recognizer