from google.cloud import vision
from vision_client import load_image_bytes
from vision_models import ImageSafety

client = vision.ImageAnnotatorClient()


def score_image_safety(image_path: str) -> ImageSafety:
    image_bytes = load_image_bytes(image_path)
    image = vision.Image(content=image_bytes)
    response = client.safe_search_detection(image=image)
    annotations = response.safe_search_annotation
    return {
        "adult": annotations.adult.name,
        "medical": annotations.medical.name,
        "racy": annotations.racy.name,
        "violence": annotations.violence.name,
    }
