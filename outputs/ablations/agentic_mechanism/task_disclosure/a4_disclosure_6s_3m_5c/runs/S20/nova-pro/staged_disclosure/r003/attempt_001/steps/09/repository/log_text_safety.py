import os
from googleapiclient.discovery import build


def check_text_safety(text):
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
    log_message = 'Example log message to check'
    safety_score = check_text_safety(log_message)
    print(f'Safety score: {safety_score}')
