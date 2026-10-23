from google.cloud import vision
import vision_client


def score_image_safety(image_path: str) -> dict[str, str]:
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=vision_client.get_image_bytes(image_path))
    response = client.safe_search_detection(image=image)
    ss = response.safe_search_annotation
    return {
        "adult": ss.adult,
        "medical": ss.medical,
        "racy": ss.racy,
        "spoof": ss.spoof,
        "violence": ss.violence,
    }
