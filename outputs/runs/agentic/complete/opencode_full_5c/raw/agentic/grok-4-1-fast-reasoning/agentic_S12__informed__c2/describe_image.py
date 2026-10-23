from vision_client import call_vision_model
from vision_models import normalize_description


def describe_image(image_url: str) -> str:
    prompt = "Generate a short visual description of the image in 1-2 sentences."
    text = call_vision_model(image_url, prompt)
    return normalize_description(text)
