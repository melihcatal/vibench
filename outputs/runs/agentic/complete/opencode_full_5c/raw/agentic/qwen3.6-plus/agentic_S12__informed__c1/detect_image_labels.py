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
    LabelDetectionRequest,
    LabelDetectionResponse,
    ImageLabel,
    normalize_label_confidence,
    parse_labels_from_qwen_vl_text,
)

DASHSCOPE_VISION_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
QWEN_VL_MODEL = "qwen-vl-max"

LABEL_DETECTION_PROMPT = (
    "Analyze this image and return a list of detected objects and labels. "
    "Format each line as 'label_name: confidence_score' where confidence_score is between 0 and 1. "
    "Return only the labels with no additional text."
)


def detect_image_labels(
    image_url: str,
    max_labels: int = 20,
    confidence_threshold: float = 0.5,
) -> LabelDetectionResponse:
    """Detect labels and objects in a static image using DashScope Qwen-VL.

    Uses the qwen-vl-max model hosted on DashScope (Alibaba Cloud).
    Requires DASHSCOPE_API_KEY environment variable.
    """
    config = VisionClientConfig(model=QWEN_VL_MODEL)
    config.validate()

    request = LabelDetectionRequest(
        image_url=image_url,
        max_labels=max_labels,
        confidence_threshold=confidence_threshold,
    )

    payload = build_vision_payload(
        model=config.model,
        image_url=request.image_url,
        prompt=LABEL_DETECTION_PROMPT,
        max_tokens=512,
        temperature=0.1,
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

    raw_text = extract_text_from_response(response_json)
    labels = parse_labels_from_qwen_vl_text(
        raw_text, threshold=request.confidence_threshold
    )
    labels = labels[: request.max_labels]

    return LabelDetectionResponse(
        labels=labels,
        image_url=request.image_url,
        model=QWEN_VL_MODEL,
        raw_response=response_json,
    )


if __name__ == "__main__":
    test_url = os.environ.get("TEST_IMAGE_URL", "https://example.com/test.jpg")
    result = detect_image_labels(test_url)
    print(
        json.dumps(
            {
                "labels": [
                    {"name": l.name, "confidence": l.confidence} for l in result.labels
                ]
            }
        )
    )
