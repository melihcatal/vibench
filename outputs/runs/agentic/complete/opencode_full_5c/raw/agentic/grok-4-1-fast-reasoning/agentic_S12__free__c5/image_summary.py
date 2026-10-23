import os
import json
from openai import OpenAI
from typing import Dict, Any


def image_summary(analyses: Dict[str, Any]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""Summarize the image analyses concisely:

{json.dumps(analyses, indent=2)}

{{"summary": "brief overview", "highlights": ["key1", "key2"]}}"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)
