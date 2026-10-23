import json
from safety_client import get_anthropic_client
from safety_models import RedactionResult


def redact_unsafe(text: str) -> RedactionResult:
    client = get_anthropic_client()
    if client is None:
        raise ValueError("Anthropic API key not configured")
    prompt = f"""Identify any unsafe, harmful, or policy-violating content spans in the following text. 
Replace those spans with [REDACTED]. Provide the full redacted text and a list of redacted spans with start index, end index, and category.

Respond ONLY with valid JSON:
{{
  "redacted_text": "full redacted text here",
  "spans": [
    {{
      "start": 12,
      "end": 25,
      "category": "harassment"
    }}
  ]
}}

Text to moderate: {text}"""
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )
    content_text = message.content[0].text.strip()
    # Find JSON
    if "{" in content_text:
        start_idx = content_text.find("{")
        end_idx = content_text.rfind("}") + 1
        json_str = content_text[start_idx:end_idx]
        data = json.loads(json_str)
        return RedactionResult(redacted_text=data["redacted_text"], spans=data["spans"])
    raise ValueError("No valid JSON response from model")
