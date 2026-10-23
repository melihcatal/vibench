from google.cloud import vision
import os

def detect_text(image_content: bytes) -> str:
    """Detects text in the image using Google Cloud Vision OCR."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        # The first annotation is the full text detected in the image.
        return texts[0].description
    else:
        return "No text detected."

if __name__ == '__main__':
    print("Running detect_image_text.py example...")
    dummy_image_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0cIDATx\xda\xed\xc1\x01\x01\x00\x00\x00\xc2\xa0\xf7Om\x00\x00\x00\x00IEND\xaeB`\x82" # A tiny valid PNG
    
    # For a real run, you'd load an image with text, e.g., an image of a sign.
    # For demonstration, we're using a tiny valid PNG byte string which likely won't have text.
    text = detect_text(dummy_image_content)
    print("Detected text:", text)
