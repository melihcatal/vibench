from vision_client import get_vision_client

def score_image_safety(image_path):
    client = get_vision_client()
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = {'content': content}
    response = client.image_annotator().safeSearchDetection(image=image).execute()
    safety = response['safeSearchAnnotation']
    return {'adult': safety['adult'],'medical': safety['medical'],'spoof': safety['spoof'], 'violence': safety['violence'], 'racy': safety['racy']}
