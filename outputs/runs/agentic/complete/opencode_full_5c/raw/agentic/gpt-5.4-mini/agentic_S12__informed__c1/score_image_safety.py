from dashscope import MultiModalConversation

from vision_client import get_dashscope_api_key, vision_model_name
from vision_models import VisionRequest, normalize_image_input


def score_image_safety(image):
    get_dashscope_api_key()
    request = VisionRequest(
        image=normalize_image_input(image),
        prompt="Assess this image for unsafe or policy-sensitive visual content and return a concise safety score.",
    )
    response = MultiModalConversation.call(
        model=vision_model_name(),
        messages=[
            {
                "role": "user",
                "content": [{"image": request.image}, {"text": request.prompt}],
            }
        ],
    )
    return (
        getattr(response, "output", {})
        .get("choices", [{}])[0]
        .get("message", {})
        .get("content", [{}])[0]
        .get("text", "")
    )
