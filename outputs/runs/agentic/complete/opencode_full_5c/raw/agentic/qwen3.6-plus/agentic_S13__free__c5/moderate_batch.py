from safety_client import get_openai_client, MODERATION_MODEL
from safety_models import BatchModerationResult, parse_batch_moderation_response


def moderate_batch(texts: list[str]) -> BatchModerationResult:
    client = get_openai_client()
    response = client.moderations.create(
        model=MODERATION_MODEL,
        input=texts,
    )
    raw = response.model_dump()
    return parse_batch_moderation_response(texts, raw)


def get_flagged_messages(texts: list[str]) -> list[str]:
    result = moderate_batch(texts)
    return [r.text for r in result.results if r.flagged]


def get_batch_summary(texts: list[str]) -> dict:
    result = moderate_batch(texts)
    return {
        "total": result.total_items,
        "flagged": result.total_flagged,
        "clean": result.total_items - result.total_flagged,
        "flagged_texts": [r.text for r in result.results if r.flagged],
    }


def moderate_batch_with_scores(texts: list[str]) -> list[dict]:
    result = moderate_batch(texts)
    return [
        {
            "text": r.text,
            "flagged": r.flagged,
            "highest_category": r.highest_category,
            "highest_score": r.highest_score,
        }
        for r in result.results
    ]
