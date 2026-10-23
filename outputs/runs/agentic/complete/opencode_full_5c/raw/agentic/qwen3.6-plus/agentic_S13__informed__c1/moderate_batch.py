from typing import Optional

from safety_models import (
    ModerationRequest,
    ModerationResponse,
    BatchModerationRequest,
    BatchModerationResponse,
    response_to_dict,
)
from safety_client import moderate_single


def moderate_batch(
    messages: list[dict],
    user_ids: Optional[list[str]] = None,
) -> dict:
    requests = []
    for i, msg in enumerate(messages):
        if isinstance(msg, str):
            text = msg
            uid = user_ids[i] if user_ids else None
        else:
            text = msg.get("text", "")
            uid = msg.get("user_id") or (user_ids[i] if user_ids else None)
        requests.append(ModerationRequest(text=text, user_id=uid))

    results = []
    for req in requests:
        response = moderate_single(req)
        results.append(response)

    flagged_count = sum(1 for r in results if r.decision.value != "allow")
    blocked_count = sum(1 for r in results if r.decision.value == "block")

    batch_response = BatchModerationResponse(
        results=results,
        total=len(results),
        flagged_count=flagged_count,
        blocked_count=blocked_count,
    )

    return {
        "results": [response_to_dict(r) for r in batch_response.results],
        "total": batch_response.total,
        "flagged_count": batch_response.flagged_count,
        "blocked_count": batch_response.blocked_count,
    }


def moderate_batch_with_details(
    messages: list[str],
    include_raw_scores: bool = True,
) -> dict:
    result = moderate_batch(messages)
    if not include_raw_scores:
        for r in result["results"]:
            r.pop("raw_scores", None)
    return result
