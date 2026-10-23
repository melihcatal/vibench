import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


class PromptSafetyError(RuntimeError):
    pass


def _call_openai_moderation(text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise PromptSafetyError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODERATION_MODEL, "input": text},
        timeout=30,
    )
    if response.status_code >= 400:
        raise PromptSafetyError(f"OpenAI moderation request failed: {response.status_code} {response.text}")
    return response.json()


def check_prompt_safety(prompt: str, generated_text: str = "", api_key: Optional[str] = None) -> Dict[str, Any]:
    combined_text = prompt if not generated_text else f"PROMPT:\n{prompt}\n\nGENERATED_TEXT:\n{generated_text}"
    data = _call_openai_moderation(combined_text, api_key=api_key)
    results = data.get("results", [])
    if not results:
        raise PromptSafetyError("OpenAI moderation returned no results")

    result = results[0]
    flagged = bool(result.get("flagged", False))
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})

    return {
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "raw": data,
    }


def is_safe(prompt: str, generated_text: str = "", api_key: Optional[str] = None) -> bool:
    return not check_prompt_safety(prompt, generated_text=generated_text, api_key=api_key)["flagged"]
