from typing import Any, Dict, List
from openai import OpenAI
import os


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Summarizes retrieved document records using OpenAI's GPT-4 model."""
    summaries = []

    for record in records:
        record_body = record.get("body", {})
        text_content = " ".join(
            [str(v) for v in record_body.values() if isinstance(v, (str, int, float))]
        )

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Summarize the following document in 2-3 sentences.",
                },
                {"role": "user", "content": text_content},
            ],
            max_tokens=100,
        )

        summary = response.choices[0].message.content.strip()
        summaries.append({"id": record["id"], "summary": summary})

    return summaries
