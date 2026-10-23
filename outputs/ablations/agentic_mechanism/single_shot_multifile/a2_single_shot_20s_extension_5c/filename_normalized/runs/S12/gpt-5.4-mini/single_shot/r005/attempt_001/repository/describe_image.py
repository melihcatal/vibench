from typing import Any, Dict

from google.cloud import vision

from vision_client import load_vision_config, open_image_bytes, vision_client
from vision_models import normalize_description_response, resolve_input_path


def describe_image(image_path: str, max_results: int = 3) -> Dict[str, Any]:
    load_vision_config()
    path = resolve_input_path(image_path)
    with open_image_bytes(path) as content:
        image = vision.Image(content=content)
        client = vision_client()
        response = client.image_properties(image=image)
        label_response = client.label_detection(image=image, max_results=max_results)
        annotation = client.object_localization(image=image)
    return normalize_description_response(
        image_path=path,
        properties=response,
        labels=label_response,
        objects=annotation,
        provider="google_cloud_vision",
    )
