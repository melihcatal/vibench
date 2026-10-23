import os
import requests

# Perspective API setup
api_key = os.getenv('PERSPECTIVE_API_KEY')

# Function to moderate profile text
def moderate_text(text):
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=' + api_key
    data = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {} }
    }
    response = requests.post(url, json=data)
    return response.json()