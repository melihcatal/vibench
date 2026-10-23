
from google.cloud import vision
import os

def extract_text_from_image(image_path):
    """Extracts plain text from a scanned document image using Google Cloud Vision API."""

    # Set up Google Cloud Vision client
    # Make sure your GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate otherwise as per Google Cloud documentation.
    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    return document.text

if __name__ == '__main__':
    # Replace 'path/to/your/scanned_document.png' with the actual path to your image
    # For example, if you have an image named 'document.png' in the same directory:
    # image_file_path = 'document.png'
    
    # You might need to set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # to the path of your service account key file before running this script:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"

    image_file_path = 'your_scanned_document_image.png'  # <<< IMPORTANT: Change this to your image path

    if not os.path.exists(image_file_path):
        print(f"Error: Image file not found at '{image_file_path}'")
        print("Please update 'image_file_path' in the script to point to your scanned document image.")
    else:
        extracted_text = extract_text_from_image(image_file_path)
        print("Extracted Text:")
        print(extracted_text)
