from safety_client import (
    get_openai_client,
    validate_batch_input,
    OPENAI_MODERATION_MODEL,
)
from safety_models import ModerationResult, BatchModerationRequest


def moderate_batch(texts, message_ids=None):
    validated = validate_batch_input(texts)
    if message_ids is not None and len(message_ids) != len(validated):
        raise ValueError("message_ids length must match texts length")
    client = get_openai_client()
    response = client.moderations.create(
        input=validated,
        model=OPENAI_MODERATION_MODEL,
    )
    results = []
    for i, result in enumerate(response.results):
        mid = message_ids[i] if message_ids and i < len(message_ids) else None
        results.append(
            ModerationResult.from_openai_response(
                text=validated[i],
                result=result,
                message_id=mid,
            )
        )
    return results


def moderate_batch_request(request):
    texts = [m.text for m in request.messages]
    message_ids = [m.message_id for m in request.messages]
    return moderate_batch(texts, message_ids)


def moderate_batch_sequential(texts, message_ids=None):
    validated = validate_batch_input(texts)
    if message_ids is not None and len(message_ids) != len(validated):
        raise ValueError("message_ids length must match texts length")
    client = get_openai_client()
    results = []
    for i, text in enumerate(validated):
        response = client.moderations.create(
            input=text,
            model=OPENAI_MODERATION_MODEL,
        )
        result = response.results[0]
        mid = message_ids[i] if message_ids and i < len(message_ids) else None
        results.append(
            ModerationResult.from_openai_response(
                text=text,
                result=result,
                message_id=mid,
            )
        )
    return results


def filter_flagged(results):
    return [r for r in results if r.flagged]


def filter_allowed(results):
    return [r for r in results if not r.flagged]


def get_batch_stats(results):
    total = len(results)
    flagged = sum(1 for r in results if r.flagged)
    return {
        "total": total,
        "flagged": flagged,
        "allowed": total - flagged,
        "flagged_rate": flagged / total if total > 0 else 0.0,
    }
