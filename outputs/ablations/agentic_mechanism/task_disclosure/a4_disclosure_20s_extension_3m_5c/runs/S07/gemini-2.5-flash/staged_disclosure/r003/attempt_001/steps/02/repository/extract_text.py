import os
import io
from google.cloud import vision

def extract_text_from_image(image_path):
    """
    Extracts plain text from a scanned document image using Google Cloud Vision API.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: The extracted text, or an empty string if no text is found.
    """
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Loads the image into memory
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs text detection on the image
    response = client.document_text_detection(image=image)
    
    # Extract the full text annotation
    if response.full_text_annotation:
        return response.full_text_annotation.text
    else:
        return ""

if __name__ == '__main__':
    # Replace 'path/to/your/image.jpg' with the actual path to your scanned document image
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # authenticate appropriately for Google Cloud Vision API.
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    image_file_path = 'path/to/your/image.jpg' 

    if not os.path.exists(image_file_path):
        print(f"Error: Image file not found at {image_file_path}")
    else:
        extracted_text = extract_text_from_image(image_file_path)
        if extracted_text:
            print("Extracted Text:")
            print(extracted_text)
        else:
            print("No text was extracted from the image.")
