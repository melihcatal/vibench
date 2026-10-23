import boto3

def check_unsafe_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        TextSegments=[
            {
                'Text': text
            }
        ]
    )
    toxic_content = response['ResultList'][0]['ToxicityScore']
    return toxic_content > 0.5