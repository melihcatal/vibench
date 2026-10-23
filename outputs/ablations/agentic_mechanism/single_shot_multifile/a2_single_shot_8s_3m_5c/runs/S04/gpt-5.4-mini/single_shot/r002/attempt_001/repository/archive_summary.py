from typing import Any, Dict

from openai import OpenAI

from speech_client import get_openai_client


def archive_summary(transcript: str) -> Dict[str, Any]:
    client = get_openai_client()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "Summarize the transcription for archival metadata."},
            {"role": "user", "content": transcript},
        ],
    )
    return {"summary": response.output_text, "provider": "openai", "model": "gpt-4.1-mini"}
