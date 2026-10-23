import os
from google.cloud import vision

def detect_image_text(image_content: bytes) -> list[str]:
    """Detects text appearing inside an image using Google Cloud Vision."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.text_detection(image=image)
    texts = [text.description for text in response.text_annotations]
    
    # The first element in text_annotations is usually the full detected text.
    if texts:
        return [texts[0]] # Return only the full detected text, or process as needed
    return []

if __name__ == '__main__':
    # Example usage (replace with actual image content)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # For demonstration, creating a dummy image content with "Hello" text
    # A tiny PNG with "Hello" would be complex to embed, so using a simple dummy.
    # In a real scenario, you'd feed an image with text.
    dummy_image_content_with_text = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0cIDATx\xda\xed\xc1\x01\x01\x00\x00\x00\xc2\xa0\xf7Om\x00\x00\x00\x00IEND\xaeB`\x82'

    try:
        detected_text = detect_image_text(dummy_image_content_with_text)
        print(f"Detected Text: {detected_text}")
    except Exception as e:
        print(f"Error detecting text: {e}")
        print("Please ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set and points to a valid service account key file.")
