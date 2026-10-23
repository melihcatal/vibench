import os
from google.cloud import vision

def score_image_safety(image_uri):
    """Detects unsafe content in the image.
    Args:
        image_uri: The URI of the image to analyze (e.g., "gs://cloud-samples-data/vision/label/wakeupcat.jpg").
    Returns:
        A dictionary containing the safety ratings for various categories.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = (
        "UNKNOWN",
        "VERY_UNLIKELY",
        "UNLIKELY",
        "POSSIBLE",
        "LIKELY",
        "VERY_LIKELY",
    )

    safety_scores = {
        "adult": likelihood_name[safe_search.adult],
        "racy": likelihood_name[safe_search.racy],
        "medical": likelihood_name[safe_search.medical],
        "violence": likelihood_name[safe_search.violence],
        "spoof": likelihood_name[safe_search.spoof],
    }

    return safety_scores

if __name__ == "__main__":
    # Example usage (replace with your image URI)
    # Ensure you have authenticated with Google Cloud, e.g., by running 'gcloud auth application-default login'
    # and have the VISION_API_KEY environment variable or a service account configured.
    # For local testing, you might need to set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    # A publicly accessible image from Google Cloud Storage
    image_to_check = "gs://cloud-samples-data/vision/label/wakeupcat.jpg"
    print(f"Checking safety for image: {image_to_check}")
    scores = score_image_safety(image_to_check)
    for category, score in scores.items():
        print(f"{category}: {score}")
