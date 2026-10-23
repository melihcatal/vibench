from typing import Any, Dict, List

from openai import OpenAI

from safety_client import get_openai_client


def moderation_summary(decisions: List[Dict[str, Any]]) -> Dict[str, Any]:
    client = get_openai_client()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize moderation decisions for an operations dashboard. Return concise JSON with summary, risk_count, allow_count, and notable_categories.",
            },
            {
                "role": "user",
                "content": str(decisions),
            },
        ],
        text={"format": {"type": "json_object"}},
    )
    return {"summary": response.output_text}
