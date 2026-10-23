from safety_client import call_moderation, OPENAI_MODERATION_MODEL
from safety_models import (
    BatchModerationRequest,
    BatchModerationResult,
    ModerationResult,
    normalize_moderation_response,
    truncate_text,
)


def moderate_batch(texts, model=None):
    request = BatchModerationRequest(texts=texts)
    results = []
    for text in request.texts:
        truncated = truncate_text(text)
        raw_response = call_moderation(
            truncated, model=model or OPENAI_MODERATION_MODEL
        )
        result = normalize_moderation_response(raw_response)
        results.append(result)
    flagged_count = sum(1 for r in results if r.flagged)
    return BatchModerationResult(
        results=results,
        total=len(results),
        flagged_count=flagged_count,
    )


def moderate_batch_with_details(texts, model=None):
    request = BatchModerationRequest(texts=texts)
    batch_result = moderate_batch(request.texts, model=model or OPENAI_MODERATION_MODEL)
    detailed = []
    for idx, result in enumerate(batch_result.results):
        detailed.append(
            {
                "index": idx,
                "text_preview": request.texts[idx][:100],
                "flagged": result.flagged,
                "categories": result.categories,
                "category_scores": [
                    {"name": cs.name, "score": cs.score, "flagged": cs.flagged}
                    for cs in result.category_scores
                ],
            }
        )
    return {
        "total": batch_result.total,
        "flagged_count": batch_result.flagged_count,
        "allowed_count": batch_result.total - batch_result.flagged_count,
        "results": detailed,
    }
