import json
from model_client import get_anthropic_client
from typing import Dict, Any


def extract_json(text: str) -> Dict[str, Any]:
    client = get_anthropic_client()
    prompt = f"""Extract the key information from the text as structured JSON.

Only output valid JSON, no other text.

Text:
{text}"""
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0.1,
        messages=[{"role": "user", "content": prompt}],
    )
    content = response.content[0].text.strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {}
