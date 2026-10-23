
import os
from google.cloud import vision

def score_image_safety(image_uri: str):
    """Checks an image for unsafe or policy-sensitive visual content."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation

    safety_scores = {
        'adult': safe_search.adult.name,
        'spoof': safe_search.spoof.name,
        'medical': safe_search.medical.name,
        'violence': safe_search.violence.name,
        'racy': safe_search.racy.name,
    }
    return safety_scores

if __name__ == '__main__':
    # This example requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    # For a real application, use an appropriate image URI.
    test_image_uri = os.environ.get("TEST_IMAGE_URI_SAFETY", "https://cloud.google.com/vision/docs/images/bike.png")
    print(f"Scoring safety for: {test_image_uri}")
    scores = score_image_safety(test_image_uri)
    print("Safety Scores:")
    for category, likelihood in scores.items():
        print(f"- {category}: {likelihood}")
