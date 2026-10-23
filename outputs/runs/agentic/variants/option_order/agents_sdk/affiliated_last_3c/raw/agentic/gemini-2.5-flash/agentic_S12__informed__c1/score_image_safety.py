from google.cloud import vision
import os

def score_image_safety(image_uri: str):
    """Checks an image for unsafe or policy-sensitive visual content using Safe Search Detection."""
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
    # This is an example, replace with a real image URI
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    image_uri = "gs://cloud-samples-data/vision/label/wakeupcat.jpg"
    safety_scores = score_image_safety(image_uri)
    print(f"Safety scores for {image_uri}: {safety_scores}")

    # Note: For actual testing of unsafe content, you would need to provide an image with such content.
