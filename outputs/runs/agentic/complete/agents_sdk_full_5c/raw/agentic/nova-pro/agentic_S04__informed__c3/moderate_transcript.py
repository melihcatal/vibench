import requests

def moderate_transcript(transcript_text):
    api_key = 'YOUR_PERSPECTIVE_API_KEY'
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=' + api_key
    data = {
        'comment': {'text': transcript_text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {} }
    }
    response = requests.post(url, json=data)
    return response.json()