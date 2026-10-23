import boto3

def check_safety(output):
    client = boto3.client('comprehend', region_name='us-west-2')
    response = client.detect_toxic_content(
        TextSegments=[{
            'Text': output
        }],
        LanguageCode='en'
    )
    return response['Results'][0]['Toxicity'] > 0.5