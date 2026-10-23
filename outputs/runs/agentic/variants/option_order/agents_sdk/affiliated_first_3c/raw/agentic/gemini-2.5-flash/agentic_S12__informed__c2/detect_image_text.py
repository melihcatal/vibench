import os
from google.cloud import vision

def detect_image_text(image_uri: str) -> list[str]:
    """Detects text in the image located in Google Cloud Storage or on the Web."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.text_detection(image=image)
    texts = [text.description for text in response.text_annotations]
    
    # The first annotation is the overall text detected in the image
    if texts:
        return texts[0].split('\n') # Return individual lines of text
    return []

if __name__ == '__main__':
    # Example usage (replace with a valid image URI with text)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    image_uri = "gs://cloud-samples-data/vision/text/sign.jpg"
    print(f"Detecting text for {image_uri}:")
    detected_texts = detect_image_text(image_uri)
    print(detected_texts)
