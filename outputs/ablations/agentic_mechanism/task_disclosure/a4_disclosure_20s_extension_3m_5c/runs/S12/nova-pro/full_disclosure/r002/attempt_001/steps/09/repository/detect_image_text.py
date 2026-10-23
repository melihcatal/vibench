from google.cloud import vision

def detect_text(image_path):
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print(f'Detected text: {text.description}')
        print(f'Confidence: {text.confidence}')
        vertices = (f'({vertex.x}, {vertex.y}) for vertex in text.bounding_poly.vertices)
        print(f'Bounding poly vertices: {vertices}')

    if response.error.message:
        raise Exception(response.error.message)

if __name__ == '__main__':
    detect_text('path_to_image.jpg')