
import io
import os

from google.cloud import vision_v1p1beta1 as vision

def detect_labels(image_path):
    """Detects labels in the image file."""
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)

if __name__ == '__main__':
    # Replace 'path/to/your/image.jpg' with the actual path to your image file
    # For example: detect_labels('test_image.jpg')
    # Or, if running from a specific directory, you might need an absolute path
    # For this example, let's assume a local image 'example_image.jpg'
    # Make sure you have an image file at this path for the script to run
    print("Please provide an image path to the detect_labels function.")
    print("Example: detect_labels('example_image.jpg')")
    # detect_labels('example_image.jpg') # Uncomment and provide a valid path to run
