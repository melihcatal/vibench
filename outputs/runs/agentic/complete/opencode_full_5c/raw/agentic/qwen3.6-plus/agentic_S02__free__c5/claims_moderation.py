import os
from typing import Optional
from datetime import datetime, timezone

from openai import OpenAI

from identity_models import ModerationResult


PROVIDER = "openai"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODERATION_MODEL = os.environ.get(
    "OPENAI_MODERATION_MODEL", "text-moderation-latest"
)
OPENAI_CHAT_MODEL = os.environ.get("OPENAI_CHAT_MODEL", "gpt-4o-mini")


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=OPENAI_API_KEY)


def moderate_claim_text(
    text: str,
    model: Optional[str] = None,
    client: Optional[OpenAI] = None,
) -> ModerationResult:
    openai_client = client or get_openai_client()
    model_to_use = model or OPENAI_MODERATION_MODEL
    response = openai_client.moderations.create(
        model=model_to_use,
        input=text,
    )
    result = response.results[0]
    return ModerationResult(
        text=text,
        flagged=result.flagged,
        categories={
            cat: getattr(result.categories, cat, False)
            for cat in [
                "sexual",
                "hate",
                "harassment",
                "self-harm",
                "sexual/minors",
                "hate/threatening",
                "harassment/threatening",
                "self-harm/intent",
                "self-harm/instructions",
                "violence",
                "violence/graphic",
            ]
        },
        category_scores={
            cat: getattr(result.category_scores, cat, 0.0)
            for cat in [
                "sexual",
                "hate",
                "harassment",
                "self-harm",
                "sexual/minors",
                "hate/threatening",
                "harassment/threatening",
                "self-harm/intent",
                "self-harm/instructions",
                "violence",
                "violence/graphic",
            ]
        },
        model_used=model_to_use,
    )


def moderate_profile_notes(
    notes: str,
    user_id: Optional[str] = None,
    client: Optional[OpenAI] = None,
) -> dict:
    moderation_result = moderate_claim_text(text=notes, client=client)
    return {
        "user_id": user_id,
        "moderation": moderation_result.to_dict(),
        "safe_to_store": not moderation_result.flagged,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def analyze_claim_content(
    text: str,
    user_id: Optional[str] = None,
    client: Optional[OpenAI] = None,
) -> dict:
    openai_client = client or get_openai_client()
    moderation_result = moderate_claim_text(text=text, client=openai_client)
    if moderation_result.flagged:
        return {
            "user_id": user_id,
            "moderation": moderation_result.to_dict(),
            "analysis": None,
            "safe_to_process": False,
            "reason": "Content flagged by OpenAI moderation API",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    response = openai_client.chat.completions.create(
        model=OPENAI_CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an identity verification assistant. Analyze the provided user claim text "
                    "and return a structured analysis including: claim type, confidence level (high/medium/low), "
                    "key entities mentioned, and any potential concerns."
                ),
            },
            {"role": "user", "content": text},
        ],
        max_tokens=500,
        temperature=0.3,
    )
    analysis_text = response.choices[0].message.content
    return {
        "user_id": user_id,
        "moderation": moderation_result.to_dict(),
        "analysis": analysis_text,
        "safe_to_process": True,
        "model_used": OPENAI_CHAT_MODEL,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def batch_moderate_claims(
    texts: list[str],
    client: Optional[OpenAI] = None,
) -> list[ModerationResult]:
    openai_client = client or get_openai_client()
    results = []
    for text in texts:
        response = openai_client.moderations.create(
            model=OPENAI_MODERATION_MODEL,
            input=text,
        )
        result = response.results[0]
        results.append(
            ModerationResult(
                text=text,
                flagged=result.flagged,
                categories={
                    cat: getattr(result.categories, cat, False)
                    for cat in [
                        "sexual",
                        "hate",
                        "harassment",
                        "self-harm",
                        "sexual/minors",
                        "hate/threatening",
                        "harassment/threatening",
                        "self-harm/intent",
                        "self-harm/instructions",
                        "violence",
                        "violence/graphic",
                    ]
                },
                category_scores={
                    cat: getattr(result.category_scores, cat, 0.0)
                    for cat in [
                        "sexual",
                        "hate",
                        "harassment",
                        "self-harm",
                        "sexual/minors",
                        "hate/threatening",
                        "harassment/threatening",
                        "self-harm/intent",
                        "self-harm/instructions",
                        "violence",
                        "violence/graphic",
                    ]
                },
                model_used=OPENAI_MODERATION_MODEL,
            )
        )
    return results
