import boto3

def check_corpus_safety(text):
    client = boto3.client('comprehend')
    response = client.detect_toxic_content(TextSegments=[{'Text': text}])
    return response['Results'][0]['Toxicity']