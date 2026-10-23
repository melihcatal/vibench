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
    ImageTextRequest,
    ImageTextResponse,
    DetectedTextRegion,
    parse_text_regions_from_qwen_vl_text,
)

DASHSCOPE_VISION_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
QWEN_VL_MODEL = "qwen-vl-max"

OCR_PROMPT = (
    "Extract all visible text from this image. Return each distinct line of text on its own line. "
    "Preserve the original language and formatting as much as possible. "
    "If no text is visible, respond with 'NO_TEXT_DETECTED'."
)


def detect_image_text(
    image_url: str,
    language_hints: list = None,
) -> ImageTextResponse:
    """Detect text appearing inside an image using DashScope Qwen-VL.

    Uses the qwen-vl-max model hosted on DashScope (Alibaba Cloud).
    Requires DASHSCOPE_API_KEY environment variable.
    """
    config = VisionClientConfig(model=QWEN_VL_MODEL)
    config.validate()

    request = ImageTextRequest(
        image_url=image_url,
        language_hints=language_hints,
    )

    prompt = OCR_PROMPT
    if request.language_hints:
        prompt += f" The text may be in the following languages: {', '.join(request.language_hints)}."

    payload = build_vision_payload(
        model=config.model,
        image_url=request.image_url,
        prompt=prompt,
        max_tokens=1024,
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

    if raw_text == "NO_TEXT_DETECTED":
        regions = []
        full_text = ""
    else:
        regions = parse_text_regions_from_qwen_vl_text(raw_text)
        full_text = "\n".join(r.text for r in regions)

    return ImageTextResponse(
        regions=regions,
        full_text=full_text,
        image_url=request.image_url,
        model=QWEN_VL_MODEL,
        raw_response=response_json,
    )


if __name__ == "__main__":
    test_url = os.environ.get("TEST_IMAGE_URL", "https://example.com/test.jpg")
    result = detect_image_text(test_url)
    print(json.dumps({"full_text": result.full_text, "regions": len(result.regions)}))
