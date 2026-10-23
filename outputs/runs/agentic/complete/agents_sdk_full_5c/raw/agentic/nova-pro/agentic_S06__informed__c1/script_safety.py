import os
import boto3

comprehend = boto3.client('comprehend')

def check_safety(text):
    result = comprehend.detect_toxic_content(TextSegments=[text])
    return result
