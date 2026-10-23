import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def summarize_moderation_decisions(decisions: List[Dict[str, Any]]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize moderation decisions concisely and clearly.",
            },
            {
                "role": "user",
                "content": f"Moderation decisions: {decisions}",
            },
        ],
    )
    return response.output_text
