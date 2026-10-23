from __future__ import annotations

from openai import OpenAI

from speech_models import SpeechResult


SUMMARY_MODEL = "gpt-4o-mini"


def archive_summary(result: SpeechResult) -> str:
    client = OpenAI()
    payload = {
        "status": result.status,
        "transcript_id": result.transcript_id,
        "segments": [segment.__dict__ for segment in result.segments],
        "text": result.text,
    }
    response = client.chat.completions.create(
        model=SUMMARY_MODEL,
        messages=[
            {"role": "system", "content": "Write a compact archival summary for a completed batch transcription job."},
            {"role": "user", "content": str(payload)},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
