from __future__ import annotations

from typing import Dict, List

from openai import OpenAI


def archive_summary(
    transcript_text: str, segments: List[Dict[str, object]]
) -> Dict[str, object]:
    client = OpenAI()
    prompt = {
        "transcript": transcript_text,
        "segments": segments,
    }
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize meeting transcripts into archive-ready JSON with summary, topics, and action_items.",
            },
            {
                "role": "user",
                "content": str(prompt),
            },
        ],
    )
    return {
        "provider": "OpenAI",
        "model": "gpt-4.1-mini",
        "summary": response.output_text,
    }
