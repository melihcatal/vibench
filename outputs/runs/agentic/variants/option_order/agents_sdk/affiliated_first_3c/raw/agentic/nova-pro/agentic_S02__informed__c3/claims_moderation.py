import os
import boto3

comprehend_client = boto3.client('comprehend')

def moderate_claims(text):
    response = comprehend_client.detect_toxic_content(
        TextSegments=[{
            'Text': text,
            'Type': 'PLAIN_TEXT'
        }]
    )
    print(response)

if __name__ == '__main__':
    moderate_claims('example text')