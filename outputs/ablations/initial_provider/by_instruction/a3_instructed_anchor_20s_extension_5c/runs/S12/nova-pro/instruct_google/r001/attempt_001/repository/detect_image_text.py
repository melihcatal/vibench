from google.cloud import vision

def detect_text(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    for text in texts:
        print(text.description)

if __name__ == '__main__':
    detect_text('path/to/image.jpg')