
import os
from google.cloud import vision_v1

def detect_text(image_path):
    """Detects text in the image file."""
    # Set up Google Cloud credentials (if not already set via environment variable GOOGLE_APPLICATION_CREDENTIALS)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/service-account-file.json"

    client = vision_v1.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision_v1.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    print('Texts:')
    for text in texts:
        print(f'\n"{text.description}"')
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])
        print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

if __name__ == '__main__':
    # Replace 'path/to/your/image.jpg' with the actual path to your image file
    # For example, if you have an image named 'test.png' in the same directory:
    # detect_text('test.png')
    print("Please provide the path to your image file as an argument to the detect_text function.")
    print("Example: detect_text('your_image_file.jpg')")
