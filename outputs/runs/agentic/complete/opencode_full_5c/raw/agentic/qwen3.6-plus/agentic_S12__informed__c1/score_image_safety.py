import json
import os
import requests
from vision_client import (
    VisionClientConfig,
    create_vision_headers,
    build_vision_payload,
    extract_text_from_response,
)
from vision_models import (
    ImageSafetyRequest,
    ImageSafetyResponse,
    SafetyCategoryScore,
    normalize_safety_score,
)

DASHSCOPE_VISION_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
QWEN_VL_MODEL = "qwen-vl-max"

SAFETY_CATEGORIES = [
    "violence",
    "adult_content",
    "gore",
    "hate_symbols",
    "self_harm",
    "drugs",
    "weapons",
    "disturbing_content",
]

SAFETY_PROMPT = (
    "Analyze this image for policy-sensitive or unsafe visual content. "
    "Evaluate each of the following categories and return a score between 0.0 (safe) and 1.0 (unsafe): "
    + ", ".join(SAFETY_CATEGORIES)
    + ".\n"
    "Format each line as 'category_name: score'. Return only the scores with no additional text."
)


def score_image_safety(
    image_url: str,
    categories: list = None,
) -> ImageSafetyResponse:
    """Check an image for unsafe or policy-sensitive visual content using DashScope Qwen-VL.

    Uses the qwen-vl-max model hosted on DashScope (Alibaba Cloud).
    Requires DASHSCOPE_API_KEY environment variable.
    """
    config = VisionClientConfig(model=QWEN_VL_MODEL)
    config.validate()

    request = ImageSafetyRequest(
        image_url=image_url,
        categories=categories or SAFETY_CATEGORIES,
    )

    prompt = (
        "Analyze this image for policy-sensitive or unsafe visual content. "
        f"Evaluate each of the following categories and return a score between 0.0 (safe) and 1.0 (unsafe): "
        + ", ".join(request.categories)
        + ".\n"
        "Format each line as 'category_name: score'. Return only the scores with no additional text."
    )

    payload = build_vision_payload(
        model=config.model,
        image_url=request.image_url,
        prompt=prompt,
        max_tokens=256,
        temperature=0.0,
    )

    headers = create_vision_headers(config.api_key)

    response = requests.post(
        DASHSCOPE_VISION_URL,
        headers=headers,
        json=payload,
        timeout=config.timeout,
    )
    response.raise_for_status()
    response_json = response.json()

    raw_text = extract_text_from_response(response_json).strip()
    category_scores = []
    overall_safe = True

    for line in raw_text.split("\n"):
        line = line.strip()
        if not line or ":" not in line:
            continue
        parts = line.split(":", 1)
        cat_name = parts[0].strip().lower()
        try:
            score = float(parts[1].strip())
        except ValueError:
            score = 0.0
        score = normalize_safety_score(score)
        label = "unsafe" if score >= 0.5 else "safe"
        if score >= 0.5:
            overall_safe = False
        category_scores.append(
            SafetyCategoryScore(
                category=cat_name,
                score=score,
                label=label,
            )
        )

    return ImageSafetyResponse(
        categories=category_scores,
        overall_safe=overall_safe,
        image_url=request.image_url,
        model=QWEN_VL_MODEL,
        raw_response=response_json,
    )


if __name__ == "__main__":
    test_url = os.environ.get("TEST_IMAGE_URL", "https://example.com/test.jpg")
    result = score_image_safety(test_url)
    print(
        json.dumps(
            {
                "overall_safe": result.overall_safe,
                "categories": [
                    {"category": c.category, "score": c.score, "label": c.label}
                    for c in result.categories
                ],
            }
        )
    )
