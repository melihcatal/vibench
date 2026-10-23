from vision_client import call_vision_model
from vision_models import normalize_labels_response, VisionAnalysis


def detect_image_labels(image_url: str) -> list[str]:
    prompt = "List the main objects, scenes, and labels detected in this image. Output only a comma-separated list of labels."
    text = call_vision_model(image_url, prompt)
    return normalize_labels_response(text)
