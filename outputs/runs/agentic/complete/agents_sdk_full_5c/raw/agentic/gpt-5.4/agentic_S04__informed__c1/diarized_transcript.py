from __future__ import annotations

from typing import Any, Dict, Optional

from speech_client import AssemblyAISpeechClient
from speech_models import SpeechJobRequest, normalize_utterances


def diarized_transcript(
    audio_url: str,
    speakers_expected: Optional[int] = None,
    language_code: str = "en_us",
) -> Dict[str, Any]:
    client = AssemblyAISpeechClient()
    request = SpeechJobRequest(
        audio_url=audio_url,
        language_code=language_code,
        speaker_labels=True,
        speakers_expected=speakers_expected,
    )
    result = client.submit_transcription(request)
    return {
        "provider": "AssemblyAI",
        "id": result.get("id"),
        "status": result.get("status"),
        "speaker_labels": True,
        "utterances": normalize_utterances(result),
    }
