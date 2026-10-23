from vision_client import (
    build_image_url,
    build_vision_messages,
    call_vision_api,
    OPENAI_VISION_MODEL,
)
from vision_models import (
    ImageAnalysisRequest,
    VisionAnalysisResponse,
    normalize_safety_result,
    build_safety_prompt,
)


def score_image_safety(
    image_path: str, model: str | None = None
) -> VisionAnalysisResponse:
    request = ImageAnalysisRequest(image_path=image_path)
    image_url = build_image_url(request.image_path)
    messages = build_vision_messages(
        system_prompt="You are a content safety evaluator that assesses images for policy violations and unsafe content.",
        user_prompt=build_safety_prompt(),
        image_url=image_url,
        detail="auto",
    )
    raw_output = call_vision_api(
        messages=messages,
        model=model or OPENAI_VISION_MODEL,
        temperature=0.0,
        max_tokens=256,
    )
    safety = normalize_safety_result(raw_output)
    return VisionAnalysisResponse(safety=safety, raw_output=raw_output)


def score_safety_from_bytes(
    image_bytes: bytes, model: str | None = None
) -> VisionAnalysisResponse:
    import base64

    encoded = base64.b64encode(image_bytes).decode("utf-8")
    image_url = f"data:image/jpeg;base64,{encoded}"
    messages = build_vision_messages(
        system_prompt="You are a content safety evaluator that assesses images for policy violations and unsafe content.",
        user_prompt=build_safety_prompt(),
        image_url=image_url,
        detail="auto",
    )
    raw_output = call_vision_api(
        messages=messages,
        model=model or OPENAI_VISION_MODEL,
        temperature=0.0,
        max_tokens=256,
    )
    safety = normalize_safety_result(raw_output)
    return VisionAnalysisResponse(safety=safety, raw_output=raw_output)


def batch_score_safety(
    image_paths: list[str], model: str | None = None
) -> list[VisionAnalysisResponse]:
    results = []
    for path in image_paths:
        result = score_image_safety(path, model=model)
        results.append(result)
    return results
