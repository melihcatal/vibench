
import os
import io
from google.cloud import vision

def detect_text(image_path):
    """Detects text in the image file."""
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print(f'\n"{text.description}"')
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])
        print('bounds: {}'.format(','.join(vertices)))

if __name__ == '__main__':
    # Replace 'path/to/your/image.jpg' with the actual path to your image file
    # For example, you can download a sample image and provide its path
    # Make sure to set up Google Cloud authentication (e.g., GOOGLE_APPLICATION_CREDENTIALS)
    # before running this script.
    
    # Example usage:
    # detect_text('path/to/your/image.jpg')
    print("Please provide an image path to the detect_text function.")
    print("Example: detect_text('your_image.jpg')")
