from google.cloud import vision
import os

def detect_text(image_content: bytes) -> str:
    """Detects text in the image content."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        # The first text annotation is usually the full detected text
        full_text = texts[0].description
        return full_text
    else:
        return ""

if __name__ == '__main__':
    # Example usage (requires an actual image binary)
    # For a real scenario, load image_content from a file or network
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"
    # with open("path/to/your/image_with_text.png", "rb") as image_file:
    #     content = image_file.read()
    #     detected_text = detect_text(content)
    #     print(f"Detected text: {detected_text}")
    pass