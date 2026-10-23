from google.cloud import vision

def detect_image_labels(image_content: bytes) -> list[str]:
    """Detects labels or objects in a static image using Google Cloud Vision API.

    Args:
        image_content: The content of the image file as bytes.

    Returns:
        A list of detected label descriptions.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]
    return labels

if __name__ == '__main__':
    # Example usage (replace with actual image content)
    # For a real application, you would load an image file:
    # with open("path/to/your/image.jpg", "rb") as image_file:
    #     content = image_file.read()
    # labels = detect_image_labels(content)
    # print("Detected labels:", labels)
    print("This script detects labels in an image using Google Cloud Vision API.")
    print("Please provide image content to the 'detect_image_labels' function.")
