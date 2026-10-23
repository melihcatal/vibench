import boto3

def check_unsafe_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(
        Text=text,
        LanguageCode='en'
    )
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return True
    return False

def check_secret_labels_and_notes(labels, notes):
    for label in labels:
        if check_unsafe_text(label):
            return True
    for note in notes:
        if check_unsafe_text(note):
            return True
    return False