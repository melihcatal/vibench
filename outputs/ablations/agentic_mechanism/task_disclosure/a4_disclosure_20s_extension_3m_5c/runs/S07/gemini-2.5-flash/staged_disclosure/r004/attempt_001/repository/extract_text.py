import os
import sys
from google.cloud import vision

def extract_text_from_image(image_path):
    """Extracts plain text from a scanned document image using Google Cloud Vision API."""

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Loads the image into memory
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs document text detection
    response = client.document_text_detection(image=image)
    texts = response.full_text_annotation

    return texts.text

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python extract_text.py <image_path>")
        sys.exit(1)

    image_file_path = sys.argv[1]
    
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json" 
    # Replace with the actual path to your Google Cloud service account key file
    
    # You should have GOOGLE_APPLICATION_CREDENTIALS environment variable set or 
    # pass the credentials explicitly in a production environment.
    # For local development, you might need to set the environment variable:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    try:
        extracted_text = extract_text_from_image(image_file_path)
        print("Extracted Text:")
        print(extracted_text)
    except Exception as e:
        print(f"An error occurred: {e}")
