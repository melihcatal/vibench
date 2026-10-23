import os
import io
from google.cloud import vision

def detect_labels(image_file):
    """Detects labels in the image file using Google Cloud Vision AI."""
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Loads the image into memory
    with io.open(image_file, 'rb') as file:
        content = file.read()

    image = vision.Image(content=content)

    # Performs label detection on the image
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('Labels:')
    for label in labels:
        print(f'{label.description}: {label.score:.2f}')

if __name__ == '__main__':
    # This is an example usage. Replace 'path/to/your/image.jpg' with your image file.
    # Make sure to set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # to the path of your service account key file.
    # Example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    # For more information, visit: https://cloud.google.com/docs/authentication/getting-started

    # For testing, you can create a dummy image file or use an existing one.
    # If you don't have one, this example will create a placeholder.
    dummy_image_path = 'example_image.jpg'
    if not os.path.exists(dummy_image_path):
        print(f"Creating a dummy file '{dummy_image_path}' for demonstration purposes.")
        print("Please replace this with a real image to get meaningful label detection.")
        with open(dummy_image_path, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\xda\xed\xc1\x01\x01\x00\x00\x00\xc2\xa0\xf7Om\x00\x00\x00\x00IEND\xaeB`\x82')
            
    detect_labels(dummy_image_path)
