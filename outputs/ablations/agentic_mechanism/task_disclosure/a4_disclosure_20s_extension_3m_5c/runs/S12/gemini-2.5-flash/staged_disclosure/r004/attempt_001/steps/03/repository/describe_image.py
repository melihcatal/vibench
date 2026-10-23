from google.cloud import vision
import os

def describe_image(image_path):
    """Generates a short visual description for an image using Google Cloud Vision AI."""

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Loads the image into memory
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs label detection on the image
    response = client.label_detection(image=image)
    labels = response.label_annotations

    description = "This image likely contains: "
    if labels:
        description += ", ".join([label.description for label in labels[:5]])  # Get top 5 labels
    else:
        description += "no clear identifiable objects."

    return description

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python describe_image.py <path_to_image>")
        sys.exit(1)

    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        sys.exit(1)

    print(f"Describing image: {image_path}")
    description = describe_image(image_path)
    print(description)
