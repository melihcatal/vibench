import json
from vision_client import extract_response_text, openai_vision_request


def score_image_safety(image_path: str):
    data = openai_vision_request(
        "Assess whether this image contains unsafe or policy-sensitive visual content. Return JSON with unsafe and categories.",
        image_path,
    )
    return json.loads(extract_response_text(data))
