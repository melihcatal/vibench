from google.cloud import vision
import io

def extract_text_from_image(image_path):
    """
    Extracts plain text from a scanned document image using Google Cloud Vision API.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: The extracted plain text.
    """
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        # The first text annotation contains the full text of the document
        return texts[0].description
    else:
        return ""

if __name__ == '__main__':
    # This is a placeholder for actual image path for demonstration purposes.
    # In a real scenario, you would provide a path to an actual image file.
    # For testing, you might create a dummy image file or use a known one.
    # Example usage:
    # extracted_text = extract_text_from_image("path/to/your/image.jpg")
    # print(extracted_text)
    pass
