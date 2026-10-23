import os
from google.cloud import vision

def extract_text(image_content: bytes) -> str:
    """Extracts plain text from a scanned document image using Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    
    if texts:
        # The first annotation is the full text of the document
        return texts[0].description
    return ""

if __name__ == '__main__':
    # This is a placeholder for demonstration. In a real scenario,
    # you would load an image from a file or another source.
    # Replace 'path/to/your/image.jpg' with a real image path.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    try:
        with open("example.png", "rb") as image_file:
            content = image_file.read()
        text = extract_text(content)
        print("Extracted Text:\n", text)
    except FileNotFoundError:
        print("Please create an 'example.png' file or replace the path with a valid image.")
    except Exception as e:
        print(f"An error occurred: {e}")
