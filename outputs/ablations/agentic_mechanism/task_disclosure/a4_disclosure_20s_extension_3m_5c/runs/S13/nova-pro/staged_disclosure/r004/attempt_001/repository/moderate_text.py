import requests

def score_text(text):
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=YOUR_API_KEY'
    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {} }
    }
    response = requests.post(url, json=payload)
    return response.json()

if __name__ == '__main__':\n    text_to_score = 'Sample text to score for toxicity.'
    result = score_text(text_to_score)
    print(result)