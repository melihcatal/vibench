from google.cloud import vision

def detect_image_labels(image_content: bytes):
    """Detects labels in the image content using Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]
    return labels

if __name__ == '__main__':
    # This is placeholder content for demonstration purposes.
    # In a real scenario, you would load an actual image.
    dummy_image_content = b"fake image data"
    print(f"Detected labels: {detect_image_labels(dummy_image_content)}")
