from google.cloud import vision
import io

def extract_text_from_image(image_path: str) -> str:
    """
    Extracts plain text from a scanned document image using Google Cloud Vision AI.

    Args:
        image_path: The path to the image file.

    Returns:
        The extracted plain text.
    """
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description
    else:
        return ""

if __name__ == '__main__':
    # Example usage:
    # You would typically have an image file here, e.g., 'document.jpg'
    # For demonstration, we'll create a dummy image file.
    # In a real scenario, replace this with a path to your actual scanned document image.

    # This part is just for testing the function locally if needed,
    # it won't be part of the final submitted code for the agent.
    pass
