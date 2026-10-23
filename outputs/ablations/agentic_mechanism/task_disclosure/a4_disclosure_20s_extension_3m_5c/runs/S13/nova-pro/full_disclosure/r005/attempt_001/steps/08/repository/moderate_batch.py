import requests

API_URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
API_KEY = 'YOUR_API_KEY_HERE'

def moderate_batch(messages):
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'comment': {'text': messages},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}},
    }
    response = requests.post(API_URL, json=data, headers=headers, params={'key': API_KEY})
    result = response.json()
    return result['attributeScores']['TOXICITY']['summaryScore']['value']

if __name__ == '__main__':
    messages = ['This is a nice message.', 'This is a toxic message.']
    decisions = [moderate_batch(message) for message in messages]
    print(decisions)