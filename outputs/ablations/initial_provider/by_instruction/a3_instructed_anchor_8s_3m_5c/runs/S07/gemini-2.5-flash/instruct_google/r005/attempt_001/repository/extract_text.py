from google.cloud import vision
import os

def extract_text_from_image(image_path: str) -> str:
    """Extracts plain text from a scanned document image using Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description
    return ""

if __name__ == "__main__":
    # Example usage: Ensure you have GOOGLE_APPLICATION_CREDENTIALS set up
    # and provide a path to a scanned document image.
    # For instance, create a dummy image file for testing.
    # This part is for local testing and not part of the core library.
    pass
