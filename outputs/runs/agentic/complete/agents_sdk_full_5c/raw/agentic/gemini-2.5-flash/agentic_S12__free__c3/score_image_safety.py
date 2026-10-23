from google.cloud import vision
import os

def score_image_safety(image_uri: str) -> dict:
    """Checks an image for unsafe content using Google Cloud Vision API Safe Search."""
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
    # This is a placeholder for actual usage.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or configure authentication.
    # Example image URI
    image_uri = os.environ.get("IMAGE_URI_SAFETY", "gs://cloud-samples-data/vision/label/wakeupcat.jpg")
    print(f"Scoring safety for image: {image_uri}")
    scores = score_image_safety(image_uri)
    print("Safety Scores:")
    for category, likelihood in scores.items():
        print(f"- {category}: {likelihood}")
