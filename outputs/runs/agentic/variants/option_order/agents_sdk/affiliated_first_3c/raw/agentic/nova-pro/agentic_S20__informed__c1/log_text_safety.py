import os
import boto3

def check_text_safety(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        TextSegments=[{
            'Text': text
        }],
        LanguageCode='en'
    )
    return response['ResultList'][0]['Toxicity'] >= 0.5
