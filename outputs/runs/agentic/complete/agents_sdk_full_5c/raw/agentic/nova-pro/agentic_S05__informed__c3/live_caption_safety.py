import requests

# Check live transcript text for unsafe content

def check_safety(text):
    response = requests.post(
        'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze',
        json={
            'comment': {'text': text},
            'languages': ['en']
        },
        params={'key': 'your-perspective-api-key'}
    )
    return response.json()