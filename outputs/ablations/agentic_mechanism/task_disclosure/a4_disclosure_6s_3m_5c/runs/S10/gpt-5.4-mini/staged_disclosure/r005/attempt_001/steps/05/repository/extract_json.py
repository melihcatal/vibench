import json
import os
import re
from typing import Any, Dict, Optional

from openai import OpenAI


def extract_json(text: str, schema_hint: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    system_prompt = (
        "Extract structured JSON from the provided text. Return only valid JSON. "
        "If schema guidance is provided, follow it strictly."
    )
    user_prompt = text if schema_hint is None else f"Schema guidance: {schema_hint}\n\nText:\n{text}"
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )
    output = response.output_text.strip()
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", output, re.DOTALL)
        if not match:
            raise ValueError("LLM did not return valid JSON")
        return json.loads(match.group(0))
