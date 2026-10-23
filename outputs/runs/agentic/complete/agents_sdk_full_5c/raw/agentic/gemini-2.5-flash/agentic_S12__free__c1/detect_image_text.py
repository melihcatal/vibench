import os
from google.cloud import vision

def detect_image_text(image_uri: str):
    """Detects text in the image located in Google Cloud Storage or on the Web."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.text_detection(image=image)
    texts = [text.description for text in response.text_annotations]
    if texts:
        # The first annotation is the aggregated text from the entire image.
        return texts[0]
    return ""

if __name__ == '__main__':
    # Example usage with a public image
    # GOOGLE_APPLICATION_CREDENTIALS must be set for local execution
    # For demonstration, a placeholder image URI is used.
    example_image_uri = "gs://cloud-samples-data/vision/text/screen.jpg"
    print(f"Detecting text for: {example_image_uri}")
    detected_text = detect_image_text(example_image_uri)
    print(f"Detected Text: {detected_text}")
