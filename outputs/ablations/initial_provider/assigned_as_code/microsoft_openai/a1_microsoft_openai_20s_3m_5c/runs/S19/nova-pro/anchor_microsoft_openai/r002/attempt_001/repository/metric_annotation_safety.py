import requests


def check_metric_annotation_safety(annotation):
    response = requests.post('https://api.perspectiveapi.com/v1/comment', json={
        'comment': {'text': annotation},
        'languages': ['en']
    }, headers={'Content-Type': 'application/json', 'Authorization': 'Bearer YOUR_API_KEY'})
    response.raise_for_status()
    data = response.json()
    safety = {
        'toxicity': data['attributeScores']['TOXICITY']['summaryScore']['value'],
        'identity_attack': data['attributeScores']['IDENTITY_ATTACK']['summaryScore']['value']
    }
    return safety