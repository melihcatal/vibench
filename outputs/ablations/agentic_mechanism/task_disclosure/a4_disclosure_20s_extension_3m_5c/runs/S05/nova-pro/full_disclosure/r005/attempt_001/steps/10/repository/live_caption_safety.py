import os
from googleapiclient.discovery import build

API_KEY = os.getenv('GOOGLE_API_KEY')

def check_safety(text):
    client = build('commentanalyzer', 'v1alpha1', developerKey=API_KEY)
    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = client.comments().analyze(body=analyze_request).execute()
    toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
    return toxicity_score > 0.5

if __name__ == '__main__':
    sample_text = 'This is a sample text to check for safety.'
    is_unsafe = check_safety(sample_text)
    print(f'Is the text unsafe? {is_unsafe}')