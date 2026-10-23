import boto3

def safety_threshold(text, threshold=0.5):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        Text=text,
        LanguageCode='en'
    )
    toxicity_score = response['Entities'][0]['Score']
    return toxicity_score < threshold