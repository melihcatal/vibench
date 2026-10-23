
from google.cloud import vision
import os

def extract_text_from_image(image_path):
    """Extracts plain text from a scanned document image using Google Cloud Vision AI.

    Args:
        image_path: The path to the image file.

    Returns:
        The extracted text from the image.
    """

    # Set up Google Cloud credentials (if not already set via GOOGLE_APPLICATION_CREDENTIALS)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"

    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    return document.text

if __name__ == '__main__':
    # Example usage:
    # Replace 'path/to/your/scanned_document.png' with the actual path to your image
    # Make sure you have set up GOOGLE_APPLICATION_CREDENTIALS environment variable
    # or uncomment and set the path to your service account key JSON file.
    # For more info: https://cloud.google.com/docs/authentication/getting-started
    
    # image_file = 'path/to/your/scanned_document.png' 
    # extracted_text = extract_text_from_image(image_file)
    # print("Extracted Text:")
    # print(extracted_text)
    print("Please replace the placeholder image path and set up Google Cloud credentials to use this script.")
