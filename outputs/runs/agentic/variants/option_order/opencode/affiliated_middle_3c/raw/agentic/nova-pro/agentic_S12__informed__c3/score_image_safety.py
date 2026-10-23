import os
from google.cloud import vision

# Instantiates a client
client = vision.ImageAnnotatorClient()


def score_safety(image_path):
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.safe_search_detection(image=image)
    safety = response.safe_search_annotation
    print("Safety Scores:")
    print("Adult:", safety.adult)
    print("Medical:", safety.medical)
    print("Violence:", safety.violence)
    print("Racy:", safety.racy)


if __name__ == "__main__":
    score_safety("path_to_image.jpg")
