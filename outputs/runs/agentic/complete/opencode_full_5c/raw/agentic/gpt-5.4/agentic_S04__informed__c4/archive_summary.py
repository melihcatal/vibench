from __future__ import annotations

import os

from openai import OpenAI


def archive_summary(transcript_text: str) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model="gpt-5.4",
        input=[
            {
                "role": "system",
                "content": "Summarize transcript content for archival retrieval with concise bullets and a short abstract.",
            },
            {"role": "user", "content": transcript_text},
        ],
    )
    return {
        "provider": "openai",
        "model": "gpt-5.4",
        "summary": response.output_text,
    }
