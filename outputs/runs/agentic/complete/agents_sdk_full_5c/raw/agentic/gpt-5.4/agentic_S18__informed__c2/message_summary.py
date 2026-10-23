from __future__ import annotations

import os
from typing import Any, Dict, List

from openai import OpenAI


OPENAI_MODEL = os.environ.get("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def summarize_processing_results(results: List[Dict[str, Any]]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "You summarize pub/sub message processing outcomes for operators in a concise operational format.",
            },
            {
                "role": "user",
                "content": f"Summarize these message processing results, highlighting failures, retries, and dead-letter outcomes: {results}",
            },
        ],
    )
    return response.choices[0].message.content or ""
