from __future__ import annotations

import os

from openai import OpenAI

from speech_models import SummaryResult, normalize_text


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_SUMMARY_MODEL = "gpt-4o-mini"


def summarize_meeting_chunk(transcript_text: str) -> SummaryResult:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(f"Missing required environment variable: {OPENAI_API_KEY_ENV}")

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=OPENAI_SUMMARY_MODEL,
        messages=[
            {
                "role": "system",
                "content": "Summarize live meeting transcript chunks into concise bullet points with decisions and action items.",
            },
            {
                "role": "user",
                "content": normalize_text(transcript_text),
            },
        ],
        temperature=0.2,
    )
    summary = response.choices[0].message.content or ""
    return SummaryResult(summary=summary.strip(), raw=response)
