import os
from typing import Dict, Any
import anthropic


def record_summary(document: Dict[str, Any]) -> str:
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = anthropic.Anthropic(api_key=anthropic_api_key)

    content_to_summarize = document.get("content", {}).get("text", "")
    if not content_to_summarize:
        return ""

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following document content: {content_to_summarize}",
            }
        ],
    )
    return response.content[0].text
