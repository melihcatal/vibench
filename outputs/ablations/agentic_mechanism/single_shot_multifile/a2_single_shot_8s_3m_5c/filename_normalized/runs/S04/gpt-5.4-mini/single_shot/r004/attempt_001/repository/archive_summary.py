from __future__ import annotations

from typing import Any, Dict, List

from speech_client import get_client


def archive_summary(transcript: str, highlights: List[str] | None = None) -> Dict[str, Any]:
    client = get_client()
    summary = transcript
    if hasattr(client, 'Summarizer'):
        summary = client.Summarizer.summarize(transcript)
    return {'summary': summary, 'highlights': highlights or []}


if __name__ == '__main__':
    raise SystemExit(0)
