import os
from google.cloud import vision

client = vision.ImageAnnotatorClient()

def score_safety(image_path):
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
        response = client.safe_search_detection(image=image)
        safety = response.safe_search_annotation
        return safety.adult, safety.violence, safety.racy, safety.medical, safety.spoof

if __name__ == '__main__':
    safety = score_safety('path_to_image.jpg')
    print(safety)