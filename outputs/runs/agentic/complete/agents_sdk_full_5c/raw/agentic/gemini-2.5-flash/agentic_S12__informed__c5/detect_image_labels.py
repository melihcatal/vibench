from google.cloud import vision
import os

def detect_labels(image_content: bytes) -> list:
    """Detects labels in the image content."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.label_detection(image=image)
    labels = []
    for label in response.label_annotations:
        labels.append(label.description)
    return labels

if __name__ == '__main__':
    # Example usage (requires an actual image binary)
    # For a real scenario, load image_content from a file or network
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"
    # with open("path/to/your/image.jpg", "rb") as image_file:
    #     content = image_file.read()
    #     detected_labels = detect_labels(content)
    #     print(f"Detected labels: {detected_labels}")
    pass