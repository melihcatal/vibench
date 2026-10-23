import os
from google.cloud import vision

def describe_image(image_content: bytes) -> str:
    """Generates a short visual description for an image using Google Cloud Vision labels."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    # Using label detection to form a description
    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]

    if labels:
        return f"The image appears to show: {', '.join(labels)}."
    else:
        return "No specific visual description could be generated."

if __name__ == '__main__':
    # Example usage (replace with actual image content)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # For demonstration, creating a dummy image content
    dummy_image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0cIDATx\xda\xed\xc1\x01\x01\x00\x00\x00\xc2\xa0\xf7Om\x00\x00\x00\x00IEND\xaeB`\x82'

    try:
        description = describe_image(dummy_image_content)
        print(f"Image Description: {description}")
    except Exception as e:
        print(f"Error describing image: {e}")
        print("Please ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set and points to a valid service account key file.")
