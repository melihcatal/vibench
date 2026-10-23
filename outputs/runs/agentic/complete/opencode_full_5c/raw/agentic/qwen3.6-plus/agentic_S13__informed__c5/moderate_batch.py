from concurrent.futures import ThreadPoolExecutor, as_completed
from safety_client import (
    call_perspective_api,
    parse_perspective_scores,
    get_perspective_api_key,
)
from safety_models import (
    ModerationRequest,
    ModerationResponse,
    BatchModerationRequest,
    BatchModerationResponse,
    CategoryScore,
)

DEFAULT_THRESHOLDS = {
    "TOXICITY": 0.7,
    "SEVERE_TOXICITY": 0.5,
    "IDENTITY_ATTACK": 0.6,
    "INSULT": 0.6,
    "PROFANITY": 0.7,
    "THREAT": 0.4,
    "SEXUALLY_EXPLICIT": 0.6,
    "FLIRTATION": 0.7,
}


def _moderate_single(
    request: ModerationRequest,
    thresholds: dict[str, float],
    api_key: str,
) -> ModerationResponse:
    raw = call_perspective_api(
        text=request.text,
        languages=request.languages,
        api_key=api_key,
    )

    raw_scores = parse_perspective_scores(raw)

    category_scores = []
    overall_violation = False

    for attr_name, score_value in raw_scores.items():
        threshold = thresholds.get(attr_name, 0.7)
        cat_score = CategoryScore(
            category=attr_name,
            score=score_value,
            threshold=threshold,
        )
        category_scores.append(cat_score)
        if cat_score.is_violating:
            overall_violation = True

    return ModerationResponse(
        text=request.text,
        scores=category_scores,
        overall_violation=overall_violation,
        provider="perspective_api",
        raw_response=raw,
    )


def moderate_batch(
    messages: list[ModerationRequest] | list[str],
    thresholds: dict[str, float] | None = None,
    api_key: str | None = None,
    max_workers: int = 5,
) -> BatchModerationResponse:
    if api_key is None:
        api_key = get_perspective_api_key()

    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS

    if isinstance(messages[0], str) if messages else False:
        requests_list = [ModerationRequest(text=m) for m in messages]
    else:
        requests_list = messages

    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_idx = {
            executor.submit(_moderate_single, req, thresholds, api_key): idx
            for idx, req in enumerate(requests_list)
        }

        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            result = future.result()
            results.append((idx, result))

    results.sort(key=lambda x: x[0])
    sorted_results = [r for _, r in results]

    return BatchModerationResponse(
        results=sorted_results,
        provider="perspective_api",
    )


if __name__ == "__main__":
    import sys

    texts = sys.argv[1:] if len(sys.argv) > 1 else ["Hello world", "You are terrible"]
    reqs = [ModerationRequest(text=t) for t in texts]
    batch_result = moderate_batch(reqs)
    print(
        f"Total: {batch_result.total_messages}, Flagged: {batch_result.flagged_count}, Clean: {batch_result.clean_count}"
    )
    for r in batch_result.results:
        print(
            f"  [{r.text[:40]}] violation={r.overall_violation} max_score={r.max_score:.4f}"
        )
