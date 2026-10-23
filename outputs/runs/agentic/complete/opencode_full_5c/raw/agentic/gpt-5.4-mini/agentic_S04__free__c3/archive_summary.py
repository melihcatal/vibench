from typing import Any, Dict, List

from openai import OpenAI

from speech_client import get_client


def archive_summary(segments: List[Dict[str, Any]]) -> Dict[str, Any]:
    client: OpenAI = get_client()
    text = "\n".join(segment.get("text", "") for segment in segments)
    result = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Summarize this transcription for archival storage:\n{text}",
    )
    return {"summary": result.output_text}
