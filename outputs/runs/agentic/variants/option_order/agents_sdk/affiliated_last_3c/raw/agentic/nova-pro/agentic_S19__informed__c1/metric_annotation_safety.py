import requests

def check_annotation_safety(text):
    response = requests.post(
        'https://api.perspectiveapi.com/v1/comment',
        headers={'Authorization': f'Bearer YOUR_PERSPECTIVE_API_KEY'},
        json={
            'comment': {
                'text': text
            },
            'languages': ['en']
        }
    )
    return response.json()