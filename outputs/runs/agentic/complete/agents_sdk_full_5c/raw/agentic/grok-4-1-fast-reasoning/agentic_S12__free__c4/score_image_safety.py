from google.cloud import vision
from vision_client import load_image_bytes
from vision_models import SafetyScores

def score_image_safety(image_path: str) -> SafetyScores:
    client = vision.ImageAnnotatorClient()
    content = load_image_bytes(image_path)
    image = vision.Image(content=content)
    response = client.safe_search_detection(image=image)
    ss_annotation = response.safe_search_annotation
    return SafetyScores(
        adult=ss_annotation.adult.name,
        racy=ss_annotation.racy.name,
        violence=ss_annotation.violence.name,
        medical=ss_annotation.medical.name,
        spoof=ss_annotation.spoof.name,
    )