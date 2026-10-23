import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def summarize_moderation_decisions(decisions: List[Dict[str, Any]], model: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model_name = model or "gpt-5.4-mini"
    response = client.responses.create(
        model=model_name,
        input=[
            {
                "role": "system",
                "content": "You summarize moderation decisions concisely and clearly.",
            },
            {
                "role": "user",
                "content": f"Summarize these moderation decisions:\n{decisions}",
            },
        ],
    )
    return response.output_text
