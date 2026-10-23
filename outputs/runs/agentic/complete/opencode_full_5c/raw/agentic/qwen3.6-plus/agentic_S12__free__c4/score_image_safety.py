from vision_client import (
    get_vision_client,
    build_vision_payload,
    parse_vision_response,
    VISION_MODEL,
)
from vision_models import SafetyScore, normalize_safety_score

VISION_MODEL_ID = "gpt-4o"

PROMPT_TEMPLATE = (
    "Evaluate the provided image for safety and policy-sensitive content. "
    "Score each category from 0.0 (safe) to 1.0 (unsafe) on a new line as: category: score. "
    "Categories to evaluate: violence, gore, adult, self_harm, hate, harassment. "
    "Return only the category scores, nothing else."
)


def score_image_safety(image_url: str = None, image_base64: str = None) -> SafetyScore:
    client = get_vision_client()
    payload = build_vision_payload(
        image_url=image_url,
        image_base64=image_base64,
        prompt=PROMPT_TEMPLATE,
    )
    response = client.chat.completions.create(**payload)
    raw_text = parse_vision_response(response)
    safety = normalize_safety_score(raw_text)
    return safety


if __name__ == "__main__":
    import sys

    image_source = sys.argv[1] if len(sys.argv) > 1 else None
    if image_source and image_source.startswith("http"):
        result = score_image_safety(image_url=image_source)
    elif image_source:
        import base64

        with open(image_source, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        result = score_image_safety(image_base64=b64)
    else:
        raise ValueError("Provide image URL or file path")
    print(f"Safe: {result.is_safe}")
    print(f"Overall score: {result.overall_score:.2f}")
    for cat, score in result.categories.items():
        print(f"  {cat}: {score:.2f}")
