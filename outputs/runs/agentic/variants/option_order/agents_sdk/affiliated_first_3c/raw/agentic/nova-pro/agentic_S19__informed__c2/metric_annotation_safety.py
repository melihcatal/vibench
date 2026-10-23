import boto3

def metric_annotation_safety(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        TextSegments=[{
            'Text': text
        }]
    )
    return response