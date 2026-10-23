import json
from vision_client import extract_response_text, openai_vision_request


def detect_image_labels(image_path: str):
    data = openai_vision_request(
        "List the visible objects and labels in this image as concise JSON array of {name,confidence}.",
        image_path,
    )
    return json.loads(extract_response_text(data))
