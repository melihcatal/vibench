from google.cloud import vision
import os

def detect_text(image_uri: str) -> list[str]:
    """Detects text in the image at the given Google Cloud Storage URI."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.text_detection(image=image)
    texts = [text.description for text in response.text_annotations]
    
    # The first annotation is the overall text detected in the image.
    # Subsequent annotations are individual words or lines.
    # We'll return all detected text descriptions.
    return texts if texts else []

if __name__ == '__main__':
    # This is a placeholder for actual usage.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or configure authentication.
    # Example image from Google Cloud Public Dataset with text
    # gs://cloud-samples-data/vision/text/screen.jpg
    image_uri = os.environ.get("IMAGE_URI_TEXT", "gs://cloud-samples-data/vision/text/screen.jpg")
    print(f"Detecting text for image: {image_uri}")
    detected_texts = detect_text(image_uri)
    print("Detected Text (first 1000 chars if long):")
    if detected_texts:
        print(detected_texts[0][:1000]) # Print the overall detected text
    else:
        print("No text detected.")
