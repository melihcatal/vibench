from vision_client import get_vision_client

def detect_image_text(image_path):
    client = get_vision_client()
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = {'content': content}
    response = client.image_annotator().textDetection(image=image).execute()
    if 'textAnnotations' in response:
        return [annotation['description'] for annotation in response['textAnnotations'] if annotation['description']!= '']
    return []
