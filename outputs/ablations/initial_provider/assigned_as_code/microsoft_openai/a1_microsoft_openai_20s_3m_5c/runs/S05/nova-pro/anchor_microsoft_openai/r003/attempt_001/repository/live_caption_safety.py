import requests

def check_safety(caption):
    url = f'https://api.perspectiveapi.com/v1alpha1/commentAnalyzer?key={os.getenv('PERSPECTIVE_API_KEY')}'
    data = {
        'comment': {'text': caption},
        'languages': ['en']
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()['attributeScores']['TOXICITY']['summaryScore']['value'] < 0.5