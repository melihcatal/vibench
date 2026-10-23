import os
import requests

def check_unsafe_content(text):
    response = requests.post(
        'https://commentanalyzer.googleapis.com/v1alpha1/perspective',
        json={
            'comment': {'text': text},
            'languages': ['en'],
            'requestedAttributes': {'TOXICITY': {}}},
        params={'key': os.getenv('PERSPECTIVE_API_KEY')}
    )
    return response.json()

if __name__ == '__main__':
    print(check_unsafe_content('This is a toxic comment.'))