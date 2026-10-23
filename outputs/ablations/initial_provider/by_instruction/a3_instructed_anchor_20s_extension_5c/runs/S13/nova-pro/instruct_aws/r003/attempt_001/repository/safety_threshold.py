import boto3

def safety_threshold(text, threshold=0.5):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(Text=text)
    if response['ToxicityScore'] > threshold:
        return False
    return True
