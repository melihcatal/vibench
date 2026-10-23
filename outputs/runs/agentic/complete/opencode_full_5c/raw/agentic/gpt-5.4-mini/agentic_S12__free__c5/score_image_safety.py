from vision_client import create_client, image_data_url, load_config
from vision_models import VisionRequest, normalize_response


def score_image_safety(
    image_bytes: bytes = None, image_url: str = None, mime_type: str = "image/png"
):
    config = load_config()
    client = create_client(config)
    request = VisionRequest(
        image_url=image_url,
        image_bytes=image_bytes,
        mime_type=mime_type,
        prompt="Assess whether this image contains unsafe, policy-sensitive, or disallowed visual content. Return a brief safety classification and rationale.",
    )
    image_source = request.image_url or image_data_url(
        request.image_bytes, request.mime_type
    )
    response = client.responses.create(
        model=config.model,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": request.prompt},
                    {"type": "input_image", "image_url": image_source},
                ],
            }
        ],
    )
    return normalize_response(response)
