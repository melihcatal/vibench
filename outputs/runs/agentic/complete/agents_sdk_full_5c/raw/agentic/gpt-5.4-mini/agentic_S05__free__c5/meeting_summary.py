from __future__ import annotations

from typing import Iterable

from speech_client import client
from speech_models import SummaryResult


def meeting_summary(chunks: Iterable[str]) -> SummaryResult:
    transcript = "\n".join(chunk.strip() for chunk in chunks if chunk.strip())
    return client.summarize_text(transcript)
