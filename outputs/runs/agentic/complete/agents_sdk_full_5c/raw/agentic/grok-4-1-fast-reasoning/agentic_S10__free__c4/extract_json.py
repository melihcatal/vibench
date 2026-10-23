import json
import os
from model_client import get_llm_client, get_model
from model_models import build_extract_prompt
from typing import Dict, Any

def extract_json(text: str, instructions: str, model_family: str = "mini") -> Dict[str, Any]:
    client = get_llm_client()
    model = get_model(model_family)
    prompt = build_extract_prompt(text, instructions)
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.0,
    )
    return json.loads(completion.choices[0].message.content)
