from google.cloud import vision
import os

def detect_labels(image_content: bytes) -> list[str]:
    """Detects labels in the image using Google Cloud Vision."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations if label.description]
    return labels

if __name__ == '__main__':
    # This is a placeholder for actual image loading.
    # In a real scenario, image_content would come from a file or network.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up for authentication.
    print("Running detect_image_labels.py example...")
    # Example: Replace with actual image bytes
    # For a real run, you'd load an image, e.g., with open("image.jpg", "rb").read()
    dummy_image_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0cIDATx\xda\xed\xc1\x01\x01\x00\x00\x00\xc2\xa0\xf7Om\x00\x00\x00\x00IEND\xaeB`\x82" # A tiny valid PNG
    
    # In a real application, you would load an actual image.
    # For demonstration, we're using a tiny valid PNG byte string.
    # You might also use vision_client.get_vision_client() if it were available here.
    
    labels = detect_labels(dummy_image_content)
    print("Detected labels:", labels)
