import boto3

def moderate_batch(texts):
    comprehend = boto3.client('comprehend')
    responses = []
    for text in texts:
        response = comprehend.detect_toxic_content(Text=text)
        responses.append(response)
    return responses
