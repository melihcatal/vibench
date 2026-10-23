import os
from googleapiclient.discovery import build

def moderate_text(text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    client = build('commentanalyzer', 'v1alpha1', developerKey=api_key)

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}}
    }

    response = client.comments().analyze(body=analyze_request).execute()

    toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
    return toxicity_score

if __name__ == '__main__':
    user_text = 'Sample text to moderate.'
    score = moderate_text(user_text)
    print(f'Toxicity score: {score}')