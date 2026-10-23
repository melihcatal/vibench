import json
import os
from openai import OpenAI


def extract_json(text: str, schema: dict | None = None) -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    system_msg = (
        "Extract structured data from the provided text and return only valid JSON. "
        "Do not include markdown code fences or any explanation."
    )
    if schema:
        system_msg += (
            f"\n\nThe JSON must conform to this schema:\n{json.dumps(schema, indent=2)}"
        )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"Extract JSON from:\n\n{text}"},
        ],
        temperature=0.1,
        max_tokens=2048,
        response_format={"type": "json_object"},
    )
    raw = response.choices[0].message.content.strip()
    return json.loads(raw)
