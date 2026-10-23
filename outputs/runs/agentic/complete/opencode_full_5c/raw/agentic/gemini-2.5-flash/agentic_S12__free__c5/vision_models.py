from google.cloud import vision_v1
import base64


def create_image_from_bytes(image_bytes: bytes) -> vision_v1.Image:
    return vision_v1.Image(content=image_bytes)


def create_image_from_uri(image_uri: str) -> vision_v1.Image:
    return vision_v1.Image(source=vision_v1.ImageSource(image_uri=image_uri))


def load_image_from_file(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


def get_text_detection_result(response) -> str:
    if response.text_annotations:
        return response.text_annotations[0].description
    return ""


def get_label_detection_results(response) -> list[str]:
    labels = []
    for label in response.label_annotations:
        labels.append(label.description)
    return labels


def get_safe_search_results(response) -> dict:
    safe_search_annotation = response.safe_search_annotation
    return {
        "adult": safe_search_annotation.adult.name,
        "racy": safe_search_annotation.racy.name,
        "medical": safe_search_annotation.medical.name,
        "violence": safe_search_annotation.violence.name,
        "spoof": safe_search_annotation.spoof.name,
    }
