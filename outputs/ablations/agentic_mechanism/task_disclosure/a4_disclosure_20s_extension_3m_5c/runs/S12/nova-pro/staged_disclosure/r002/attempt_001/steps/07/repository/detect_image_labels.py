from google.cloud import vision

def detect_labels(image_path):
    """Detects labels in the file."""
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)

    labels = response.label_annotations

    print("Labels:\n")
    for label in labels:
        print(label.description)

if __name__ == "__main__":
    image_path = "path/to/your/image.jpg"
    detect_labels(image_path)