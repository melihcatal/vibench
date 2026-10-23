from pathlib import Path
from typing import Any, Dict, List

from google.cloud import vision

from vision_models import ImageAnalysisRequest


def _load_image_bytes(image_path: str) -> bytes:
    return Path(image_path).read_bytes()


def _client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def _image_from_path(image_path: str) -> vision.Image:
    return vision.Image(content=_load_image_bytes(image_path))


def analyze_labels(request: ImageAnalysisRequest) -> List[Any]:
    client = _client()
    image = _image_from_path(request.image_path)
    response = client.label_detection(image=image, max_results=request.max_results)
    return list(response.label_annotations or [])


def analyze_text(request: ImageAnalysisRequest) -> List[Any]:
    client = _client()
    image = _image_from_path(request.image_path)
    response = client.text_detection(image=image)
    return list(response.text_annotations or [])


def analyze_safe_search(request: ImageAnalysisRequest) -> Dict[str, Any]:
    client = _client()
    image = _image_from_path(request.image_path)
    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation
    return {
        "adult": getattr(safe, "adult", None),
        "spoof": getattr(safe, "spoof", None),
        "medical": getattr(safe, "medical", None),
        "violence": getattr(safe, "violence", None),
        "racy": getattr(safe, "racy", None),
    }


def summarize_image(image_path: str) -> str:
    client = _client()
    image = _image_from_path(image_path)
    response = client.label_detection(image=image, max_results=5)
    labels = [item.description for item in response.label_annotations or []]
    return ", ".join(labels[:3])


def translate_text(text: str, target_language: str) -> str:
    from google.cloud import translate_v2 as translate

    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result.get("translatedText", text)


def archive_payload(bucket_name: str, object_name: str, payload: str) -> str:
    from google.cloud import storage

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_string(payload)
    return f"gs://{bucket_name}/{object_name}"
