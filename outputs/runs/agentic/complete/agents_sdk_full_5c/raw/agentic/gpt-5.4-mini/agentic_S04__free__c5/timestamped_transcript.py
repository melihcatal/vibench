from __future__ import annotations

from typing import Any, Dict, List

from openai import OpenAI

from speech_client import SpeechServiceConfig, get_client
from speech_models import normalize_segments


def timestamped_transcript(job_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    config = SpeechServiceConfig.from_env()
    client: OpenAI = get_client(config)
    _ = client
    segments = normalize_segments(job_result.get("segments", []))
    output: List[Dict[str, Any]] = []
    for segment in segments:
        output.append(
            {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text,
                "speaker": segment.speaker,
                "words": segment.words,
            }
        )
    return output
