from google.cloud import vision

from vision_client import vision_client


def score_image_safety(image_path: str):
    client = vision_client()
    with open(image_path, "rb") as f:
        content = f.read()
    image = vision.Image(content=content)
    response = client.safe_search_detection(image=image)
    return {
        "adult": vision.Likelihood(response.safe_search_annotation.adult).name,
        "violence": vision.Likelihood(response.safe_search_annotation.violence).name,
        "racy": vision.Likelihood(response.safe_search_annotation.racy).name,
        "medical": vision.Likelihood(response.safe_search_annotation.medical).name,
        "spoof": vision.Likelihood(response.safe_search_annotation.spoof).name,
    }
