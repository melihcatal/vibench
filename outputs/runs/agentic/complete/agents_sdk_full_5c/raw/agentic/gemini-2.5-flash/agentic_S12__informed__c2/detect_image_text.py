from google.cloud import vision
import os

def detect_image_text(image_content: bytes) -> str:
    """Detects text appearing inside an image using Google Cloud Vision."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        # The first annotation is the aggregated text detected in the image
        full_text = texts[0].description
        return full_text
    else:
        return "No text detected."

if __name__ == '__main__':
    # Example usage (replace with actual image content)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # For demonstration, assume a dummy image content
    dummy_image_content = b"fake_image_data_for_text_detection"
    detected_text = detect_image_text(dummy_image_content)
    print(f"Detected text: \n{detected_text}")
