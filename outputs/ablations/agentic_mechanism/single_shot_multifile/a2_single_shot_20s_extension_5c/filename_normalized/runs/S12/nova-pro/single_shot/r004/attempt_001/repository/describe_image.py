from vision_client import get_vision_client

def describe_image(image_path):
    client = get_vision_client()
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = {'content': content}
    response = client.image_annotator().textDetection(image=image).execute()
    if 'fullTextAnnotation' in response:
        return response['fullTextAnnotation']['text']
    return ''
