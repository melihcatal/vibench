import os
import json
from typing import Any, Dict
from anthropic import Anthropic
from model_client import extract_json_prompt


def extract_json(
    text: str, instructions: str, model: str = "claude-3-5-sonnet-20240620"
) -> Dict[str, Any]:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = extract_json_prompt(text, instructions)
    message = client.messages.create(
        model=model,
        max_tokens=2000,
        temperature=0.1,
        system="You are a precise JSON extractor. Output only valid JSON matching the instructions.",
        messages=[{"role": "user", "content": prompt}],
    )
    content = message.content[0].text
    return json.loads(content)
