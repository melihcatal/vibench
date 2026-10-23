from google.cloud import vision

def detect_labels(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')
    for label in labels:
        print(label.description, label.score)

if __name__ == '__main__':\n    detect_labels('path_to_image.jpg')