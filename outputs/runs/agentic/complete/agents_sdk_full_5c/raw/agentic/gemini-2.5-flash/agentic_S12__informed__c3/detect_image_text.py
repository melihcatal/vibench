
import os
from google.cloud import vision

def detect_image_text(image_uri: str):
    """Detects text in the image located in Google Cloud Storage or on the Web."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.text_detection(image=image)
    texts = [text.description for text in response.text_annotations]
    # The first annotation is the total detected text
    if texts:
        return texts[0]
    return "No text detected."

if __name__ == '__main__':
    # This example requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    # For a real application, consider using a path to a GCS object, e.g., "gs://cloud-samples-data/vision/text/screen.jpg"
    # or a public URL, e.g., "https://cloud.google.com/vision/docs/images/text/screen.jpg"
    test_image_uri = os.environ.get("TEST_IMAGE_URI_TEXT", "https://cloud.google.com/vision/docs/images/text/screen.jpg")
    print(f"Detecting text for: {test_image_uri}")
    detected_text = detect_image_text(test_image_uri)
    print(f"Detected text: {detected_text}")
