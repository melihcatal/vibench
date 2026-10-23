from __future__ import annotations

import os
from typing import Any

from openai import OpenAI

from database_models import summarize_records


def record_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    stats = summarize_records(records)
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Summarize these document records for operations review: {records}",
                    }
                ],
            }
        ],
    )
    return {"summary": response.output_text, "stats": stats}
