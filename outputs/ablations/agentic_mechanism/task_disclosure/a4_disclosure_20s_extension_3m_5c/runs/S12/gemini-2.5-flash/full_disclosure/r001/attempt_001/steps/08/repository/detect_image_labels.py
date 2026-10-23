from google.cloud import vision_v1
from google.cloud.vision_v1 import types

def detect_labels(image_content: bytes) -> list[str]:
    """Detects labels in the image content using Google Cloud Vision AI.

    Args:
        image_content: The content of the image file as bytes.

    Returns:
        A list of detected label descriptions.
    """
    client = vision_v1.ImageAnnotatorClient()
    image = types.Image(content=image_content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    detected_labels = []
    for label in labels:
        detected_labels.append(label.description)

    return detected_labels

if __name__ == '__main__':
    # Example usage: Replace with actual image loading
    try:
        with open("path/to/your/image.jpg", "rb") as image_file:
            content = image_file.read()
        
        labels = detect_labels(content)
        print("Labels:")
        for label in labels:
            print(f"- {label}")
    except FileNotFoundError:
        print("Error: Image file not found. Please provide a valid path to an image file.")
    except Exception as e:
        print(f"An error occurred: {e}")
