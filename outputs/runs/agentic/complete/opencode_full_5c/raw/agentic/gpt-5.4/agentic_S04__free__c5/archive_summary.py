from __future__ import annotations

from typing import Any, Dict, List

from openai import OpenAI

from speech_client import require_openai_api_key
from speech_models import SummaryResult


def archive_summary(segments: List[Dict[str, Any]]) -> Dict[str, Any]:
    client = OpenAI(api_key=require_openai_api_key())
    transcript_text = "\n".join(segment.get("text", "") for segment in segments)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Summarize this meeting transcript for archive retrieval in 5 concise bullet points:\n{transcript_text}",
    )
    result = SummaryResult(
        summary=response.output_text, provider="openai", model="gpt-4.1-mini"
    )
    return {
        "provider": result.provider,
        "model": result.model,
        "summary": result.summary,
    }
