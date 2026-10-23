from __future__ import annotations

from typing import Any, Dict, Optional

from speech_client import get_client
from speech_models import TimestampedTranscriptRequest, normalize_timestamps


def timestamped_transcript(job_id: str, *, granularity: str = 'word', include_confidence: bool = False) -> Dict[str, Any]:
    client = get_client()
    request = TimestampedTranscriptRequest(job_id=job_id, granularity=granularity, include_confidence=include_confidence)
    result = client.transcriptions.fetch_timestamps(request)
    return normalize_timestamps(result)


if __name__ == '__main__':
    raise SystemExit(0)
