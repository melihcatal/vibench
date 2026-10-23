import json
import os
from typing import Any, Dict

from openai import OpenAI


def extract_json(text: str, schema_hint: str | None = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = "Extract the requested structured JSON from the text. Return only valid JSON."
    if schema_hint:
        prompt = f"{prompt} Schema hint: {schema_hint}"
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": "You extract structured data and output only JSON.",
            },
            {
                "role": "user",
                "content": f"{prompt}\n\nText:\n{text}",
            },
        ],
        response_format={"type": "json_object"},
    )
    output_text = response.output_text
    return json.loads(output_text)


if __name__ == "__main__":
    import sys

    source_text = sys.stdin.read()
    result = extract_json(source_text)
    print(json.dumps(result, ensure_ascii=False))
