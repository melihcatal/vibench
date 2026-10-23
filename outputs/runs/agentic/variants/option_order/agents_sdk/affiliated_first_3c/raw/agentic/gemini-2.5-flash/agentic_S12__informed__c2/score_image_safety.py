import os
from google.cloud import vision

def score_image_safety(image_uri: str) -> dict:
    """Checks an image for unsafe or policy-sensitive visual content."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.safe_search_detection(image=image)
    safe_search_annotation = response.safe_search_annotation

    safety_scores = {
        'adult': safe_search_annotation.adult.name,
        'spoof': safe_search_annotation.spoof.name,
        'medical': safe_search_annotation.medical.name,
        'violence': safe_search_annotation.violence.name,
        'racy': safe_search_annotation.racy.name,
    }
    return safety_scores

if __name__ == '__main__':
    # Example usage (replace with a valid image URI)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    image_uri = "gs://cloud-samples-data/vision/label/wakeupcat.jpg"
    print(f"Scoring safety for {image_uri}:")
    safety_results = score_image_safety(image_uri)
    print(safety_results)
