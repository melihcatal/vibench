import requests

VISION_API_KEY = 'your_vision_api_key'

def detect_text(image_path):
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    response = requests.post(
        'https://vision.googleapis.com/v1/images:annotate?key=' + VISION_API_KEY,
        json={
            'requests': [{
                'image': {'content': image_data},
                'features': [{'type': 'TEXT_DETECTION'}]
            }]
        }
    )
    return response.json()['responses'][0]['textAnnotations']