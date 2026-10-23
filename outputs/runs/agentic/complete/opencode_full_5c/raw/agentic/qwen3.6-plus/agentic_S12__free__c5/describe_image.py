from vision_client import (
    build_image_url,
    build_vision_messages,
    call_vision_api,
    OPENAI_VISION_MODEL,
)
from vision_models import (
    ImageAnalysisRequest,
    VisionAnalysisResponse,
    build_description_prompt,
)


def describe_image(image_path: str, model: str | None = None) -> VisionAnalysisResponse:
    request = ImageAnalysisRequest(image_path=image_path)
    image_url = build_image_url(request.image_path)
    messages = build_vision_messages(
        system_prompt="You are a visual description assistant that creates concise, accurate image descriptions.",
        user_prompt=build_description_prompt(),
        image_url=image_url,
        detail=request.detail,
    )
    raw_output = call_vision_api(
        messages=messages,
        model=model or OPENAI_VISION_MODEL,
        temperature=0.3,
        max_tokens=256,
    )
    return VisionAnalysisResponse(description=raw_output.strip(), raw_output=raw_output)


def describe_image_from_bytes(
    image_bytes: bytes, model: str | None = None
) -> VisionAnalysisResponse:
    import base64

    encoded = base64.b64encode(image_bytes).decode("utf-8")
    image_url = f"data:image/jpeg;base64,{encoded}"
    messages = build_vision_messages(
        system_prompt="You are a visual description assistant that creates concise, accurate image descriptions.",
        user_prompt=build_description_prompt(),
        image_url=image_url,
        detail="auto",
    )
    raw_output = call_vision_api(
        messages=messages,
        model=model or OPENAI_VISION_MODEL,
        temperature=0.3,
        max_tokens=256,
    )
    return VisionAnalysisResponse(description=raw_output.strip(), raw_output=raw_output)


def batch_describe_images(
    image_paths: list[str], model: str | None = None
) -> list[VisionAnalysisResponse]:
    results = []
    for path in image_paths:
        result = describe_image(path, model=model)
        results.append(result)
    return results
