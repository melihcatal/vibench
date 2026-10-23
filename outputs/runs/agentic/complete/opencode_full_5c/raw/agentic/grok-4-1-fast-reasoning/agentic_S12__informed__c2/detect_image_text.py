from vision_client import call_vision_model
from vision_models import normalize_ocr_text


def detect_image_text(image_url: str) -> str:
    prompt = (
        "Detect and transcribe all text appearing in the image exactly as it appears."
    )
    text = call_vision_model(image_url, prompt)
    return normalize_ocr_text(text)
