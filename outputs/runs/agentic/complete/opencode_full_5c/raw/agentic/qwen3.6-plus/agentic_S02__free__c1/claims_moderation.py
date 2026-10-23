import os
from typing import Optional, Dict, Any, List

from identity_models import ModerationResult


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_MODERATION_MODEL = "omni-moderation-latest"
OPENAI_CHAT_MODEL = "gpt-4o"


def moderate_claims_text(
    text: str,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
) -> ModerationResult:
    import requests

    key = api_key or OPENAI_API_KEY
    mod_model = model or OPENAI_MODERATION_MODEL

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }

    resp = requests.post(
        f"{OPENAI_API_BASE}/moderations",
        headers=headers,
        json={"input": text, "model": mod_model},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    result = data["results"][0]
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})

    return ModerationResult(
        text=text,
        flagged=result.get("flagged", False),
        categories=categories,
        category_scores=category_scores,
        provider="openai",
        model=mod_model,
    )


def moderate_user_notes(
    notes: List[str],
    api_key: Optional[str] = None,
    model: Optional[str] = None,
) -> List[ModerationResult]:
    return [moderate_claims_text(note, api_key=api_key, model=model) for note in notes]


def moderate_with_context(
    text: str,
    context: Optional[str] = None,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    mod_result = moderate_claims_text(text, api_key=api_key, model=model)

    if mod_result.flagged and context:
        import requests

        key = api_key or OPENAI_API_KEY
        chat_model = model or OPENAI_CHAT_MODEL

        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        }

        system_prompt = (
            "You are a claims moderation assistant. Review the provided text and context "
            "to determine if the content violates acceptable use policies for identity claims."
        )

        user_message = f"Context: {context}\n\nText to review: {text}"

        resp = requests.post(
            f"{OPENAI_API_BASE}/chat/completions",
            headers=headers,
            json={
                "model": chat_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                "max_tokens": 500,
                "temperature": 0.0,
            },
            timeout=60,
        )
        resp.raise_for_status()
        chat_data = resp.json()
        analysis = chat_data["choices"][0]["message"]["content"]
    else:
        analysis = None

    return {
        "moderation_result": {
            "text": mod_result.text,
            "flagged": mod_result.flagged,
            "categories": mod_result.categories,
            "category_scores": mod_result.category_scores,
        },
        "contextual_analysis": analysis,
        "provider": "openai",
        "moderation_model": mod_result.model,
        "chat_model": OPENAI_CHAT_MODEL if mod_result.flagged else None,
    }


def batch_moderate_claims(
    claims: List[Dict[str, Any]],
    text_field: str = "notes",
    api_key: Optional[str] = None,
    model: Optional[str] = None,
) -> List[Dict[str, Any]]:
    results = []
    for claim in claims:
        text = claim.get(text_field, "")
        if not text:
            continue
        mod = moderate_claims_text(text, api_key=api_key, model=model)
        results.append(
            {
                "claim_id": claim.get("id", claim.get("sub", "")),
                "moderation": {
                    "flagged": mod.flagged,
                    "categories": mod.categories,
                    "category_scores": mod.category_scores,
                    "model": mod.model,
                },
            }
        )
    return results
