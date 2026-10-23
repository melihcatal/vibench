import json
import os
from typing import Any, Dict, Optional

from openai import OpenAI


def extract_json(text: str, schema_hint: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model_name = model or os.environ.get("OPENAI_JSON_EXTRACTOR_MODEL", "gpt-4o-mini")
    instructions = "Extract the requested structured information from the text and return only valid JSON."
    if schema_hint:
        instructions += f" Use this schema guidance: {schema_hint}"
    response = client.responses.create(
        model=model_name,
        input=[
            {
                "role": "system",
                "content": instructions,
            },
            {
                "role": "user",
                "content": text,
            },
        ],
    )
    output = response.output_text.strip()
    return json.loads(output)
