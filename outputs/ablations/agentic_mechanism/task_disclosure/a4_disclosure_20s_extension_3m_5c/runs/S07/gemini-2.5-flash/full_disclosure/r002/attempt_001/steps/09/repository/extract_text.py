from google.cloud import vision

def extract_text_from_image(image_content: bytes) -> str:
    """
    Extracts plain text from a scanned document image using Google Cloud Vision AI.

    Args:
        image_content: The content of the image file in bytes.

    Returns:
        The extracted plain text.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description
    return ""

if __name__ == '__main__':
    # This is an example of how to use the function.
    # Replace 'path/to/your/image.jpg' with the actual path to your image file.
    # You will need to install the Google Cloud Vision AI client library:
    # pip install google-cloud-vision
    # Make sure you have authenticated to Google Cloud.
    try:
        with open('path/to/your/image.jpg', 'rb') as image_file:
            content = image_file.read()
        extracted_text = extract_text_from_image(content)
        print("Extracted Text:")
        print(extracted_text)
    except FileNotFoundError:
        print("Error: image file not found. Please update the path and ensure the file exists.")
    except Exception as e:
        print(f"An error occurred: {e}")
