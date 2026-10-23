from google.cloud import vision
import os

def detect_labels(image_content: bytes) -> list[str]:
    """Detects labels in the image content using Google Cloud Vision."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]
    return labels

if __name__ == '__main__':
    # Example usage (replace with actual image content)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # For demonstration, assume a dummy image content
    dummy_image_content = b"fake_image_data_for_labels"
    detected_labels = detect_labels(dummy_image_content)
    print(f"Detected labels: {detected_labels}")
