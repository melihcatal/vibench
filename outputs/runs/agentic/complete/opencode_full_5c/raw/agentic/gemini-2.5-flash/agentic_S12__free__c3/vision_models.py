import base64
from google.cloud import vision_v1


def encode_image_to_base64(image_path_or_bytes):
    """Encodes an image to a base64 string, handling both file paths and byte data."""
    if isinstance(image_path_or_bytes, str):
        with open(image_path_or_bytes, "rb") as image_file:
            content = image_file.read()
    else:
        content = image_path_or_bytes
    return base64.b64encode(content).decode("utf-8")


def create_vision_image(image_path_or_bytes):
    """Creates a Vision API Image object from a file path or bytes."""
    if isinstance(image_path_or_bytes, str):
        with open(image_path_or_bytes, "rb") as image_file:
            content = image_file.read()
    else:
        content = image_path_or_bytes
    return vision_v1.Image(content=content)


def parse_label_detection_response(response):
    """Parses the label detection response from Vision API."""
    labels = []
    if response.label_annotations:
        for label in response.label_annotations:
            labels.append(label.description)
    return labels


def parse_text_detection_response(response):
    """Parses the text detection response from Vision API."""
    texts = []
    if response.text_annotations:
        for text in response.text_annotations:
            texts.append(text.description)
    return texts


def parse_safe_search_detection_response(response):
    """Parses the safe search detection response from Vision API."""
    safe_search_annotation = response.safe_search_annotation
    return {
        "adult": safe_search_annotation.adult.name,
        "spoof": safe_search_annotation.spoof.name,
        "medical": safe_search_annotation.medical.name,
        "violence": safe_search_annotation.violence.name,
        "racy": safe_search_annotation.racy.name,
    }
