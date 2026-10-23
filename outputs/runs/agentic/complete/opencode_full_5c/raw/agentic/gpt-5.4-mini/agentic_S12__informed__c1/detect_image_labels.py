import os

from dashscope import MultiModalConversation

from vision_client import get_dashscope_api_key, vision_model_name
from vision_models import VisionRequest, normalize_image_input, normalize_text_list


def detect_image_labels(image):
    get_dashscope_api_key()
    request = VisionRequest(
        image=normalize_image_input(image),
        prompt="Identify labels and visible objects in this image.",
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
    text = (
        getattr(response, "output", {})
        .get("choices", [{}])[0]
        .get("message", {})
        .get("content", [{}])[0]
        .get("text", "")
    )
    return normalize_text_list(text.split(","))
