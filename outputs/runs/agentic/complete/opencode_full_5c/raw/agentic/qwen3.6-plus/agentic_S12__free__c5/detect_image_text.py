from vision_client import (
    build_image_url,
    build_vision_messages,
    call_vision_api,
    OPENAI_VISION_MODEL,
)
from vision_models import (
    ImageAnalysisRequest,
    VisionAnalysisResponse,
    normalize_detected_text,
    build_text_detection_prompt,
)


def detect_image_text(
    image_path: str, model: str | None = None
) -> VisionAnalysisResponse:
    request = ImageAnalysisRequest(image_path=image_path)
    image_url = build_image_url(request.image_path)
    messages = build_vision_messages(
        system_prompt="You are an OCR and text detection assistant that extracts all visible text from images.",
        user_prompt=build_text_detection_prompt(),
        image_url=image_url,
        detail="high",
    )
    raw_output = call_vision_api(
        messages=messages,
        model=model or OPENAI_VISION_MODEL,
        temperature=0.0,
        max_tokens=1024,
    )
    detected_text = normalize_detected_text(raw_output)
    return VisionAnalysisResponse(detected_text=detected_text, raw_output=raw_output)


def detect_text_from_bytes(
    image_bytes: bytes, model: str | None = None
) -> VisionAnalysisResponse:
    import base64

    encoded = base64.b64encode(image_bytes).decode("utf-8")
    image_url = f"data:image/jpeg;base64,{encoded}"
    messages = build_vision_messages(
        system_prompt="You are an OCR and text detection assistant that extracts all visible text from images.",
        user_prompt=build_text_detection_prompt(),
        image_url=image_url,
        detail="high",
    )
    raw_output = call_vision_api(
        messages=messages,
        model=model or OPENAI_VISION_MODEL,
        temperature=0.0,
        max_tokens=1024,
    )
    detected_text = normalize_detected_text(raw_output)
    return VisionAnalysisResponse(detected_text=detected_text, raw_output=raw_output)


def batch_detect_text(
    image_paths: list[str], model: str | None = None
) -> list[VisionAnalysisResponse]:
    results = []
    for path in image_paths:
        result = detect_image_text(path, model=model)
        results.append(result)
    return results
