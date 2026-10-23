from google.cloud import vision

def detect_labels(image_path):
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    print("Labels:")
    for label in labels:
        print(label.description)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python detect_image_labels.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    detect_labels(image_path)
