import boto3

def moderate_batch(texts):
    comprehend = boto3.client('comprehend')
    results = []
    for text in texts:
        response = comprehend.detect_toxic_content(Text=text)
        results.append(response)
    return results