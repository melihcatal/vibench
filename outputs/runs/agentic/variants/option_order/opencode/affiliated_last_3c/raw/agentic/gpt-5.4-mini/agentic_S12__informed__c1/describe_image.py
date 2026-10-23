from vision_client import dashscope_request, load_image_source
from vision_models import normalize_text


def describe_image(image_path=None, image_bytes=None, image_url=None):
    image = load_image_source(
        image_path=image_path, image_bytes=image_bytes, image_url=image_url
    )
    result = dashscope_request("Write a short visual description of this image.", image)
    content = (
        getattr(result, "output", {})
        .get("choices", [{}])[0]
        .get("message", {})
        .get("content", [])
    )
    return normalize_text(content)
