import os
from google.cloud import vision

def score_image_safety(image_uri: str):
    """Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision API."""
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
    # Example usage with a public image
    # GOOGLE_APPLICATION_CREDENTIALS must be set for local execution
    # For demonstration, a placeholder image URI is used.
    example_image_uri = "gs://cloud-samples-data/vision/label/wakeupcat.jpg"
    print(f"Scoring safety for: {example_image_uri}")
    safety_results = score_image_safety(example_image_uri)
    print(f"Safety Scores: {safety_results}")
