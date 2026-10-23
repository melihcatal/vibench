from google.cloud import vision
import os

def detect_text(image_path):
    """Detects text in the image file."""
    # Set up Google Cloud credentials (if not already set via GOOGLE_APPLICATION_CREDENTIALS)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/credentials.json"

    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    print('Texts:')
    for text in texts:
        print(f'\n"{text.description}"')
        print('Bounds:')
        vertices = ([f'({vertex.x},{vertex.y})'
                    for vertex in text.bounding_poly.vertices])
        print(' '.join(vertices))

    if response.error.message:
        raise Exception(
            '{}
For more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

if __name__ == '__main__':
    # Replace with the path to your image file
    # For example, download an image with text and put its path here
    # Example: detect_text('path/to/your/image.jpg')
    print("Please provide an image path to the detect_text function.")
