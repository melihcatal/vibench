import requests

VISION_API_KEY = 'your_vision_api_key'

def detect_labels(image_path):
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    response = requests.post(
        'https://vision.googleapis.com/v1/images:annotate?key=' + VISION_API_KEY,
        json={
            'requests': [{
                'image': {'content': image_data},
                'features': [{'type': 'LABEL_DETECTION'}]
            }]
        }
    )
    return response.json()['responses'][0]['labelAnnotations']