import os

from google.cloud import vision


class VisionClient:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def analyze_image(self, image_path):
        with open(image_path, 'rb') as image_file:
            image = vision.Image(content=image_file.read())
            response = self.client.label_detection(image=image)
            labels = response.label_annotations
            return labels

if __name__ == '__main__':
    client = VisionClient()
    labels = client.analyze_image('path_to_image.jpg')
    for label in labels:
        print(label.description, label.score)