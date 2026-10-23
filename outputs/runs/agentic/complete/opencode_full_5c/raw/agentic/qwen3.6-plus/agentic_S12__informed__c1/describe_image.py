import json
import os
import requests
from vision_client import (
    VisionClientConfig,
    create_vision_headers,
    build_vision_payload,
    extract_text_from_response,
)
from vision_models import ImageDescriptionRequest, ImageDescriptionResponse

DASHSCOPE_VISION_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
QWEN_VL_MODEL = "qwen-vl-max"

DESCRIPTION_PROMPTS = {
    "brief": "Describe this image in 2-3 concise sentences. Focus on the main subjects, setting, and notable visual details.",
    "detailed": "Provide a detailed description of this image. Cover the main subjects, background, colors, lighting, composition, and any notable visual elements.",
    "alt_text": "Write a concise alt-text description of this image suitable for accessibility, in one sentence.",
}


def describe_image(
    image_url: str,
    detail_level: str = "brief",
    language: str = "en",
) -> ImageDescriptionResponse:
    """Generate a short visual description for an image using DashScope Qwen-VL.

    Uses the qwen-vl-max model hosted on DashScope (Alibaba Cloud).
    Requires DASHSCOPE_API_KEY environment variable.
    """
    config = VisionClientConfig(model=QWEN_VL_MODEL)
    config.validate()

    request = ImageDescriptionRequest(
        image_url=image_url,
        detail_level=detail_level,
        language=language,
    )

    prompt = DESCRIPTION_PROMPTS.get(detail_level, DESCRIPTION_PROMPTS["brief"])
    if language != "en":
        prompt += f" Respond in {language}."

    payload = build_vision_payload(
        model=config.model,
        image_url=request.image_url,
        prompt=prompt,
        max_tokens=256,
        temperature=0.2,
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

    description = extract_text_from_response(response_json).strip()

    return ImageDescriptionResponse(
        description=description,
        image_url=request.image_url,
        model=QWEN_VL_MODEL,
        raw_response=response_json,
    )


if __name__ == "__main__":
    test_url = os.environ.get("TEST_IMAGE_URL", "https://example.com/test.jpg")
    result = describe_image(test_url)
    print(json.dumps({"description": result.description}))
