from __future__ import annotations

from openai import OpenAI

from speech_client import OPENAI_SUMMARY_MODEL, get_client, normalize_text
from speech_models import SummaryRequest


def archive_summary(transcript: str, max_tokens: int = 256) -> dict:
    client: OpenAI = get_client()
    request = SummaryRequest(transcript=normalize_text(transcript), max_tokens=max_tokens)
    response = client.responses.create(
        model=OPENAI_SUMMARY_MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Summarize this transcription result in under {request.max_tokens} tokens for archival purposes:\n\n{request.transcript}",
                    }
                ],
            }
        ],
    )
    return {"summary": response.output_text, "raw": response.model_dump()}
