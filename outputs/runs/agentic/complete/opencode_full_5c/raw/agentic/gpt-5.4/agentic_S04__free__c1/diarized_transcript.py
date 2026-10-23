from __future__ import annotations

from typing import Any, Dict, List, Optional

from speech_client import AssemblyAIClient, build_transcription_request


def request_diarized_meeting_transcript(
    audio_url: str,
    speaker_count: Optional[int] = None,
    language_code: Optional[str] = None,
) -> Dict[str, Any]:
    client = AssemblyAIClient()
    request = build_transcription_request(
        audio_url=audio_url,
        language_code=language_code,
        speaker_labels=True,
        speaker_count=speaker_count,
    )
    result = client.submit_transcription(request)
    return {
        "provider": "AssemblyAI",
        "feature": "speaker_labels",
        "transcript_id": result.transcript_id,
        "status": result.status,
    }


def extract_diarized_turns(transcript_id: str) -> List[Dict[str, Any]]:
    client = AssemblyAIClient()
    result = client.get_transcription(transcript_id)
    return [
        {
            "speaker": segment.speaker,
            "text": segment.text,
            "start_ms": segment.start_ms,
            "end_ms": segment.end_ms,
            "confidence": segment.confidence,
        }
        for segment in result.segments
    ]
