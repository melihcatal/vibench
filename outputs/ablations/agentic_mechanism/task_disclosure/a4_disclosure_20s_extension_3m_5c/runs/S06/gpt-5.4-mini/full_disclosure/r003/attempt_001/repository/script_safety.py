import json
import os
from typing import Any, Dict, Optional

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_SAFETY_MODEL", "gpt-4.1-mini")


def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def check_script_safety(script: str, locale: Optional[str] = None) -> Dict[str, Any]:
    prompt = [
        "Assess the following narration script for unsafe content.",
        "Return strict JSON with keys: unsafe (boolean), categories (array of strings), rationale (string).",
        "Consider hate, harassment, sexual content, self-harm, violence, illegal wrongdoing, and sensitive content.",
    ]
    if locale:
        prompt.append(f"Target locale: {locale}")
    prompt.append(f"Script: {script}")
    response = _client().responses.create(
        model=OPENAI_MODEL,
        input="\n".join(prompt),
        temperature=0,
    )
    text = response.output_text.strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        data = {"unsafe": False, "categories": [], "rationale": text}
    data.setdefault("unsafe", False)
    data.setdefault("categories", [])
    data.setdefault("rationale", "")
    return data


def is_script_safe(script: str, locale: Optional[str] = None) -> bool:
    return not bool(check_script_safety(script, locale).get("unsafe", False))
