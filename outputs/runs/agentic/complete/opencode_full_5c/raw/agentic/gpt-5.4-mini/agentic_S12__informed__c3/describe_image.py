from typing import Any, Dict

from google.cloud import vision

from vision_client import client, image_input


def describe_image(source: str, max_results: int = 1) -> Dict[str, Any]:
    annotator = client()
    image = image_input(source)
    response = annotator.web_detection(image=image)
    desc = ""
    if response.web_detection and response.web_detection.best_guess_labels:
        desc = response.web_detection.best_guess_labels[0].label
    return {"description": desc, "model": "google-cloud-vision"}
