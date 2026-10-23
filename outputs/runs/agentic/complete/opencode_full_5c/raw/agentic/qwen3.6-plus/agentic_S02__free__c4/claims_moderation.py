import os
import json
import requests
from typing import Optional, Dict, Any, List
from identity_models import (
    ClaimsModerationRequest,
    ClaimsModerationResult,
)


OPENAI_API_URL = "https://api.openai.com/v1"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"
OPENAI_CHAT_MODEL = "gpt-4o-mini"


def moderate_claims_with_openai(
    text: str,
    api_key: Optional[str] = None,
    model: str = OPENAI_MODERATION_MODEL,
) -> ClaimsModerationResult:
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY", "")

    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    body = {
        "model": model,
        "input": text,
    }

    response = requests.post(
        f"{OPENAI_API_URL}/moderations",
        headers=headers,
        json=body,
        timeout=30,
    )
    response.raise_for_status()
    result_data = response.json()

    result_obj = result_data.get("results", [{}])[0]
    flagged = result_obj.get("flagged", False)
    categories = result_obj.get("category_scores", {})
    category_applied_action = result_obj.get("categories", {})

    action_map = {}
    for cat, is_flagged in category_applied_action.items():
        if is_flagged:
            action_map[cat] = "block"
        else:
            action_map[cat] = "allow"

    confidence = max(categories.values()) if categories else 0.0

    return ClaimsModerationResult(
        flagged=flagged,
        categories={k: float(v) for k, v in categories.items()},
        category_applied_action={
            k: action_map.get(k, "allow") for k in category_applied_action
        },
        confidence=confidence,
        raw_response=result_data,
    )


def moderate_federated_claims(
    claims_text: str,
    user_sub: Optional[str] = None,
    context: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY", "")

    moderation_result = moderate_claims_with_openai(
        text=claims_text,
        api_key=api_key,
    )

    metadata = {}
    if user_sub:
        metadata["user_sub"] = user_sub
    if context:
        metadata["context"] = context

    return {
        "success": True,
        "moderation": {
            "flagged": moderation_result.flagged,
            "categories": moderation_result.categories,
            "category_actions": moderation_result.category_applied_action,
            "confidence": moderation_result.confidence,
        },
        "metadata": metadata,
    }


def moderate_notes_with_openai_chat(
    notes: List[str],
    api_key: Optional[str] = None,
    model: str = OPENAI_CHAT_MODEL,
) -> List[Dict[str, Any]]:
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY", "")

    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    system_prompt = (
        "You are a content moderation assistant for federated identity claims. "
        "Analyze each note for policy violations including: harassment, hate speech, "
        "self-harm, sexual content, violence, and illegal activity. "
        "Return a JSON array with objects containing: note_index, flagged (boolean), "
        "reason (string if flagged), severity (low|medium|high)."
    )

    user_content = "Moderate the following notes:\n"
    for i, note in enumerate(notes):
        user_content += f"[{i}] {note}\n"

    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.0,
    }

    response = requests.post(
        f"{OPENAI_API_URL}/chat/completions",
        headers=headers,
        json=body,
        timeout=30,
    )
    response.raise_for_status()
    result_data = response.json()

    content = result_data["choices"][0]["message"]["content"]
    parsed = json.loads(content)

    results = parsed.get("results", [])
    return results


def batch_moderate_claims(
    requests_list: List[ClaimsModerationRequest],
    api_key: Optional[str] = None,
) -> List[ClaimsModerationResult]:
    results = []
    for req in requests_list:
        result = moderate_claims_with_openai(
            text=req.text,
            api_key=api_key,
        )
        result.explanation = (
            f"Moderation for user {req.user_sub or 'unknown'}"
            if req.user_sub
            else "Moderation completed"
        )
        results.append(result)
    return results
