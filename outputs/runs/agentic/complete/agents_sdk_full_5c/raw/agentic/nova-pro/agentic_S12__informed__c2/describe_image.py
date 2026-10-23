import os
from google.cloud import vision

client = vision.ImageAnnotatorClient()

def describe_image(image_path):
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
        response = client.label_detection(image=image)
        description = response.label_annotations[0].description if response.label_annotations else 'No description found.'
        return description

if __name__ == '__main__':
    description = describe_image('path_to_image.jpg')
    print(description)