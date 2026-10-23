import os

from google.cloud import vision
from google.cloud.vision import types

def check_safety(text):
    client = vision.ImageAnnotatorClient()

    # Convert the text content to features
    feature = types.Feature(type=types.Feature.Type.WEB_DETECTION)
    image = types.Image(content=text.encode('utf-8'))
    request = types.AnnotateImageRequest(image=image, features=[feature])

    # Perform the web detection request
    response = client.annotate_image(request)

    # Check if the response contains any unsafe content
    if response.web_detection.adult_content_likelihood!= vision.Likelihood.VERY_UNLIKELY:
        return 'Unsafe content detected'
    else:
        return 'Safe content'

if __name__ == '__main__':
    # Example usage
    text = 'This is a sample narration script.'
    result = check_safety(text)
    print(result)