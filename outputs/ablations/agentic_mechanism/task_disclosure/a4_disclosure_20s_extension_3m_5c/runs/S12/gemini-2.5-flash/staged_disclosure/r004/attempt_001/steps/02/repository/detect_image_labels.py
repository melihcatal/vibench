from google.cloud import vision
import os

def detect_labels(image_path):
    """Detects labels in the image using Google Cloud Vision AI."""

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Loads the image into memory
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs label detection on the image
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print("Labels:")
    for label in labels:
        print(f"- {label.description} (score: {label.score:.2f})")

if __name__ == "__main__":
    # Replace 'path/to/your/image.jpg' with the actual path to your image file
    # Ensure you have authenticated to Google Cloud and set up the GOOGLE_APPLICATION_CREDENTIALS
    # environment variable, or use `gcloud auth application-default login`.
    image_file = "path/to/your/image.jpg"
    if os.path.exists(image_file):
        detect_labels(image_file)
    else:
        print(f"Error: Image file not found at {image_file}. Please update the image_file variable.")
        print("For example: image_file = 'my_image.jpg'")
        print("You can also set the GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication.")
