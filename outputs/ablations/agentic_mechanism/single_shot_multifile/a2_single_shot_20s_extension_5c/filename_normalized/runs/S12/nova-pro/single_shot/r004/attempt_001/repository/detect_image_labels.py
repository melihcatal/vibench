from vision_client import get_vision_client

def detect_image_labels(image_path):
    client = get_vision_client()
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = {'content': content}
    response = client.image_annotator().labelDetection(image=image).execute()
    labels = response['labelAnnotations']
    return [{'description': label['description'],'score': label['score']} for label in labels]
