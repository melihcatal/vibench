import boto3

def check_corpus_text(text):
    comprehend = boto3.client('comprehend')
    toxic_content_detected = False
    try:
        response = comprehend.detect_toxic_content(
            Text=text,
            LanguageCode='en'
        )
        if response['Labels']:
            toxic_content_detected = True
    except Exception as e:
        print(f"Error detecting toxic content: {e}")
    return not toxic_content_detected