import os
from typing import Any, Dict, List

from openai import OpenAI


def summarize_audit_events(events: List[Dict[str, Any]]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"))
    prompt = {"events": events}
    response = client.responses.create(model="gpt-5.4-mini", input=[{"role": "user", "content": str(prompt)}])
    return response.output_text
