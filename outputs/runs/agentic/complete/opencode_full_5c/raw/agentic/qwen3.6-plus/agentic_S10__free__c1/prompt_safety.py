from model_client import create_openai_client, load_config
from model_models import SafetyCheckRequest, SafetyCheckResponse


def check_safety(
    text: str,
    model: str = "omni-moderation-latest",
) -> SafetyCheckResponse:
    req = SafetyCheckRequest(text=text, model=model)
    config = load_config()
    client = create_openai_client()

    moderation = client.moderations.create(
        input=req.text,
        model=req.model,
    )

    result = moderation.results[0]
    flagged = result.flagged

    categories = {}
    category_scores = {}
    for cat_name in result.categories.model_fields_set:
        cat_value = getattr(result.categories, cat_name, None)
        if cat_value is not None:
            categories[cat_name] = cat_value

    for score_name in result.category_scores.model_fields_set:
        score_value = getattr(result.category_scores, score_name, None)
        if score_value is not None:
            category_scores[score_name] = score_value

    return SafetyCheckResponse(
        flagged=flagged,
        categories=categories,
        category_scores=category_scores,
        model=moderation.model,
        raw=moderation.model_dump(),
    )


def is_safe(text: str, model: str = "omni-moderation-latest") -> bool:
    result = check_safety(text, model=model)
    return not result.flagged


if __name__ == "__main__":
    import sys

    input_text = sys.stdin.read() if not sys.stdin.isatty() else ""
    if input_text:
        result = check_safety(input_text)
        print(f"Flagged: {result.flagged}")
        print(f"Categories: {result.categories}")
