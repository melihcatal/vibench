import requests

VISION_API_KEY = 'YOUR_VISION_API_KEY'

def describe_image(image_path):
    url = 'https://vision.googleapis.com/v1/images:annotate?key=' + VISION_API_KEY
    headers = {'Content-Type': 'application/json'}
    payload = {
        'requests': [{
            'image': {'content': open(image_path, 'rb').read().decode('utf-8')},
            'features': [{'type': 'DOCUMENT_TEXT_DETECTION'}]
        }]
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()['responses'][0]['fullTextAnnotation']['text']