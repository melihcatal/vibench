import os
from google.cloud import vision

def extract_text_from_image(image_path: str) -> str:
    """Extracts plain text from a scanned document image using Google Cloud Vision API.

    Args:
        image_path: The path to the image file.

    Returns:
        The extracted plain text.
    """
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description
    return ""

if __name__ == '__main__':
    # This is a placeholder for actual image path and credential setup.
    # For local execution, ensure GOOGLE_APPLICATION_CREDENTIALS is set
    # or pass credentials explicitly.
    # Example: python extract_text.py /path/to/your/image.jpg
    # Make sure you have an image file for testing.
    # For actual usage, you would typically pass the image_path from another part of your application.
    if len(os.sys.argv) > 1:
        image_file_path = os.sys.argv[1]
        extracted_text = extract_text_from_image(image_file_path)
        print("Extracted Text:")
        print(extracted_text)
    else:
        print("Please provide an image path as an argument.")
        print("Usage: python extract_text.py <path_to_image.jpg>")
