import os
from google.cloud import vision

def detect_image_labels(image_content: bytes) -> list[str]:
    """Detects labels in the image content using Google Cloud Vision."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]
    return labels

if __name__ == '__main__':
    # Example usage (replace with actual image content)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # For demonstration, creating a dummy image content
    dummy_image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0cIDATx\xda\xed\xc1\x01\x01\x00\x00\x00\xc2\xa0\xf7Om\x00\x00\x00\x00IEND\xaeB`\x82'
    
    # In a real scenario, you would read an image file:
    # with open("path/to/your/image.jpg", "rb") as image_file:
    #     image_content = image_file.read()

    try:
        labels = detect_image_labels(dummy_image_content)
        print(f"Detected Labels: {labels}")
    except Exception as e:
        print(f"Error detecting labels: {e}")
        print("Please ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set and points to a valid service account key file.")
