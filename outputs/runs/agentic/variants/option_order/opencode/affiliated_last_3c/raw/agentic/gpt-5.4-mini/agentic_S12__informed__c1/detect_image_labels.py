from vision_client import dashscope_request, load_image_source
from vision_models import normalize_labels


def detect_image_labels(image_path=None, image_bytes=None, image_url=None):
    image = load_image_source(
        image_path=image_path, image_bytes=image_bytes, image_url=image_url
    )
    result = dashscope_request(
        "Identify the main objects and labels in this image.", image
    )
    content = (
        getattr(result, "output", {})
        .get("choices", [{}])[0]
        .get("message", {})
        .get("content", [])
    )
    return normalize_labels(content)
