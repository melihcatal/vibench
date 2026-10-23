from google.cloud import vision

def detect_image_text(image_content: bytes):
    """Detects text in the image content using Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.text_detection(image=image)
    texts = [text.description for text in response.text_annotations]
    if texts:
        # The first entry in text_annotations is usually the full detected text.
        return texts[0]
    return ""

if __name__ == '__main__':
    # This is placeholder content for demonstration purposes.
    # In a real scenario, you would load an actual image.
    dummy_image_content = b"fake image data"
    print(f"Detected text: {detect_image_text(dummy_image_content)}")
