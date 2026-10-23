import boto3

def check_unsafe_content(payload_text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        TextSegments=[
            {
                'Text': payload_text
            }
        ]
    )
    for result in response['ResultList']:
        if result['Toxicity']['Label'] == 'TOXIC':
            return True
    return False