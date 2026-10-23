import json
from speech_client import get_openai_client
from speech_models import SafetyRequest, SafetyResponse, normalize_safety_request

OPENAI_SAFETY_MODEL = "gpt-4o"


def check_script_safety(
    text: str, categories: list = None, model: str = None
) -> SafetyResponse:
    client = get_openai_client()

    if model is None:
        model = OPENAI_SAFETY_MODEL

    req = SafetyRequest(text=text, categories=categories)
    messages = normalize_safety_request(req)

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.0,
        response_format={"type": "json_object"},
    )

    result_text = response.choices[0].message.content.strip()
    result_data = json.loads(result_text)

    is_safe = result_data.get("is_safe", True)
    flagged_categories = result_data.get("flagged_categories", [])
    scores = result_data.get("scores", {})

    return SafetyResponse(
        is_safe=is_safe,
        flagged_categories=flagged_categories,
        scores=scores,
        model_used=model,
    )


def check_script_safety_batch(
    texts: list, categories: list = None, model: str = None
) -> list:
    results = []
    for text in texts:
        result = check_script_safety(text, categories=categories, model=model)
        results.append(result)
    return results
