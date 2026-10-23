import json
import os
from typing import Any, Dict
from anthropic import Anthropic

def image_summary(analysis_results: Dict[str, Any]) -> str:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = (
        "Summarize the following visual analysis results in a concise paragraph:\\n\\n"
        + json.dumps(analysis_results, indent=2)
    )
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()