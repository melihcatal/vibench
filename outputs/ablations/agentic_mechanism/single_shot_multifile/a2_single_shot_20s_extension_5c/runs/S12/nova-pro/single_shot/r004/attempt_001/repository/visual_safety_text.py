from vision_client import get_vision_client

def visual_safety_text(text):
    client = get_vision_client()
    response = client.image_annotator().textDetection(image={'content': text}).execute()
    if 'textAnnotations' in response:
        for annotation in response['textAnnotations']:
            if annotation['description'] in ['unsafe','sensitive']:
                return True
    return False
