from vision_client import (
    build_image_url,
    build_vision_messages,
    call_vision_api,
    OPENAI_VISION_MODEL,
)
from vision_models import (
    ImageAnalysisRequest,
    ImageLabel,
    VisionAnalysisResponse,
    normalize_labels,
    build_label_prompt,
)


def detect_image_labels(
    image_path: str, model: str | None = None
) -> VisionAnalysisResponse:
    request = ImageAnalysisRequest(image_path=image_path)
    image_url = build_image_url(request.image_path)
    messages = build_vision_messages(
        system_prompt="You are an image label detection assistant.",
        user_prompt=build_label_prompt(),
        image_url=image_url,
        detail=request.detail,
    )
    raw_output = call_vision_api(
        messages=messages,
        model=model or OPENAI_VISION_MODEL,
        temperature=0.0,
        max_tokens=512,
    )
    labels = normalize_labels(raw_output)
    return VisionAnalysisResponse(labels=labels, raw_output=raw_output)


def detect_labels_from_bytes(
    image_bytes: bytes, model: str | None = None
) -> VisionAnalysisResponse:
    import base64

    encoded = base64.b64encode(image_bytes).decode("utf-8")
    image_url = f"data:image/jpeg;base64,{encoded}"
    messages = build_vision_messages(
        system_prompt="You are an image label detection assistant.",
        user_prompt=build_label_prompt(),
        image_url=image_url,
        detail="auto",
    )
    raw_output = call_vision_api(
        messages=messages,
        model=model or OPENAI_VISION_MODEL,
        temperature=0.0,
        max_tokens=512,
    )
    labels = normalize_labels(raw_output)
    return VisionAnalysisResponse(labels=labels, raw_output=raw_output)


def batch_detect_labels(
    image_paths: list[str], model: str | None = None
) -> list[VisionAnalysisResponse]:
    results = []
    for path in image_paths:
        result = detect_image_labels(path, model=model)
        results.append(result)
    return results
