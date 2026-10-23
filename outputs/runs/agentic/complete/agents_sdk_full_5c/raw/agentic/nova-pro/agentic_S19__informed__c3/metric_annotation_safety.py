import requests

def check_metric_annotation_safety(annotation):
    response = requests.post(
        'https://api.perspectiveapi.com/v1/comment',
        json={
            'comment': {
                'text': annotation
            },
            'languages': ['en']
        },
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {os.getenv("PERSPECTIVE_API_KEY")}'
        }
    )
    return response.json()