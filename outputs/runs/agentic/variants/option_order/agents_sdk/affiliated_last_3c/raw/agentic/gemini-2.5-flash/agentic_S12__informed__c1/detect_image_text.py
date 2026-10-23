from google.cloud import vision
import os

def detect_image_text(image_uri: str):
    """Detects text in the image."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.text_detection(image=image)
    texts = response.text_annotations
    
    detected_text = []
    if texts:
        # The first annotation is the total text detected
        full_text = texts[0].description
        detected_text.append(full_text)
        # Other annotations are individual words/lines
        # For simplicity, we'll just return the full text for now

    return detected_text[0] if detected_text else "No text detected."

if __name__ == 'main':
    # This is an example, replace with a real image URI
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    image_uri = "gs://cloud-samples-data/vision/text/screen.jpg"
    text = detect_image_text(image_uri)
    print(f"Text detected in {image_uri}:\n{text}")

    image_uri_2 = "gs://cloud-samples-data/vision/label/wakeupcat.jpg"
    text_2 = detect_image_text(image_uri_2)
    print(f"Text detected in {image_uri_2}:\n{text_2}")
