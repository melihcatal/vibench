import io
from google.cloud import vision

def extract_text_from_image(image_path):
    """Extracts text from an image using Google Cloud Vision AI."""

    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        # The first text_annotation is the full text from the image
        return texts[0].description
    else:
        return ""

if __name__ == '__main__':
    # This is example usage and requires an image file to run.
    # Replace 'path/to/your/image.jpg' with the actual path to your scanned document image.
    # Make sure you have authenticated to Google Cloud (e.g., gcloud auth application-default login)
    # and enabled the Vision AI API in your Google Cloud project.
    image_file = 'path/to/your/image.jpg' # Placeholder
    extracted_text = extract_text_from_image(image_file)
    print("Extracted Text:")
    print(extracted_text)
