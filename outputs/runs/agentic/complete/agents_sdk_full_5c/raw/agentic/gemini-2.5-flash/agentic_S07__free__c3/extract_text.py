from google.cloud import vision
import os

def extract_text_from_image(image_content: bytes) -> str:
    """Extracts plain text from a scanned document image using Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        return texts[0].description
    return ""

if __name__ == '__main__':
    # Example usage (requires an image file)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or authenticated
    # with open("path/to/your/image.jpg", "rb") as image_file:
    #     content = image_file.read()
    #     text = extract_text_from_image(content)
    #     print(f"Extracted Text: {text[:500]}...")
    pass
