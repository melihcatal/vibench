import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


class PromptSafetyError(RuntimeError):
    pass


def _openai_headers() -> Dict[str, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise PromptSafetyError("OPENAI_API_KEY is required")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def _moderate(text: str) -> Dict[str, Any]:
    response = requests.post(
        OPENAI_API_URL,
        headers=_openai_headers(),
        json={"model": OPENAI_MODERATION_MODEL, "input": text},
        timeout=30,
    )
    if response.status_code >= 400:
        raise PromptSafetyError(f"OpenAI moderation request failed: {response.status_code} {response.text}")
    data = response.json()
    if not isinstance(data, dict):
        raise PromptSafetyError("Invalid moderation response")
    return data


def _result_flagged(result: Dict[str, Any]) -> bool:
    flagged = result.get("flagged")
    if isinstance(flagged, bool):
        return flagged
    categories = result.get("categories")
    if isinstance(categories, dict):
        return any(bool(v) for v in categories.values())
    return False


def _result_reasons(result: Dict[str, Any]) -> List[str]:
    reasons: List[str] = []
    categories = result.get("categories")
    if isinstance(categories, dict):
        reasons.extend([name for name, value in categories.items() if value])
    category_scores = result.get("category_scores")
    if isinstance(category_scores, dict):
        reasons.extend([f"{name}:{score}" for name, score in category_scores.items() if isinstance(score, (int, float)) and score >= 0.5])
    return reasons


def check_prompt(prompt: str) -> Dict[str, Any]:
    data = _moderate(prompt)
    result = data.get("results", [{}])[0]
    if not isinstance(result, dict):
        raise PromptSafetyError("Invalid moderation result")
    return {
        "safe": not _result_flagged(result),
        "reasons": _result_reasons(result),
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
    }


def check_generated_text(text: str) -> Dict[str, Any]:
    return check_prompt(text)


def is_safe(prompt: str, generated_text: Optional[str] = None) -> bool:
    prompt_check = check_prompt(prompt)
    if not prompt_check["safe"]:
        return False
    if generated_text is not None:
        generated_check = check_generated_text(generated_text)
        if not generated_check["safe"]:
            return False
    return True


def assess_content(prompt: str, generated_text: Optional[str] = None) -> Dict[str, Any]:
    prompt_check = check_prompt(prompt)
    generated_check = check_generated_text(generated_text) if generated_text is not None else None
    return {
        "prompt": prompt_check,
        "generated_text": generated_check,
        "safe": prompt_check["safe"] and (generated_check["safe"] if generated_check is not None else True),
    }
