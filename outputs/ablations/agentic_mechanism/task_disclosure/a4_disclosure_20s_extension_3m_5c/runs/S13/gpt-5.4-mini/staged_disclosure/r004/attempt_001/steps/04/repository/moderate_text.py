import os
import json
from typing import Any, Dict

from openai import OpenAI


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def score_text(text: str) -> Dict[str, Any]:
    resp = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": "Score the user's text for unsafe or policy-violating content. Return strict JSON with keys: unsafe (boolean), risk_score (number from 0 to 1), categories (array of strings), explanation (string).",
            },
            {"role": "user", "content": text},
        ],
        response_format={"type": "json_object"},
    )
    payload = resp.output_text
    try:
        return json.loads(payload)
    except Exception:
        return {"unsafe": False, "risk_score": 0.0, "categories": [], "explanation": payload}


def moderate_text(text: str) -> Dict[str, Any]:
    return score_text(text)
