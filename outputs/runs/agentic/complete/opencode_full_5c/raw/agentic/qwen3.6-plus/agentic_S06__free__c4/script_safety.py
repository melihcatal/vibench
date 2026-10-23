import httpx
from speech_client import (
    OPENAI_MODERATIONS_ENDPOINT,
    get_openai_headers,
    create_http_client,
    build_moderation_payload,
    validate_openai_key,
)
from speech_models import SafetyCheckRequest, SafetyCheckResponse


def check_script_safety(
    text: str,
) -> SafetyCheckResponse:
    if not validate_openai_key():
        raise ValueError("OPENAI_API_KEY is not set or invalid")

    request = SafetyCheckRequest(text=text)
    payload = request.to_openai_payload()

    with create_http_client() as client:
        response = client.post(
            OPENAI_MODERATIONS_ENDPOINT,
            headers=get_openai_headers(),
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

    result = data["results"][0]
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})
    flagged = result.get("flagged", False)

    return SafetyCheckResponse(
        is_safe=not flagged,
        flagged=flagged,
        categories=categories,
        category_scores=category_scores,
        model_used=data.get("model", "text-moderation-latest"),
    )


def check_script_safety_batch(
    texts: list,
) -> list:
    results = []
    for text in texts:
        result = check_script_safety(text=text)
        results.append(result)
    return results


def check_and_filter_scripts(
    scripts: list,
) -> list:
    safe_scripts = []
    for script in scripts:
        safety_result = check_script_safety(text=script)
        if safety_result.is_safe:
            safe_scripts.append(script)
    return safe_scripts


def get_flagged_categories(
    text: str,
) -> dict:
    result = check_script_safety(text=text)
    flagged_cats = {
        cat: score
        for cat, score in result.category_scores.items()
        if result.categories.get(cat, False)
    }
    return flagged_cats
