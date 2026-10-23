import boto3

def check_annotation_safety(annotation):
    client = boto3.client('comprehend')
    response = client.detect_toxic_content(
        TextSegments=[
            {
                'Text': annotation
            }
        ]
    )
    return response