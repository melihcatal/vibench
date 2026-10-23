from google.cloud import vision

from vision_client import load_config


def detect_image_text(payload, config=None):
    cfg = load_config(config)
    client = vision.ImageAnnotatorClient()
    response = client.text_detection(
        image=vision.Image(content=payload["image_bytes"]),
        image_context=vision.ImageContext(language_hints=list(cfg.language_hints)),
    )
    if response.error.message:
        raise RuntimeError(response.error.message)
    return {"texts": [{"text": text.description, "confidence": getattr(text, "confidence", 0.0)} for text in response.text_annotations[: cfg.max_text_results]]}
