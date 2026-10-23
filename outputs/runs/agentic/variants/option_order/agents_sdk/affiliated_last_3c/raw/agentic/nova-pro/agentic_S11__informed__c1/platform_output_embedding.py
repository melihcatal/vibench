import os
import boto3

def embed_text(text):
    comprehend = boto3.client('comprehend', region_name='us-west-2')
    response = comprehend.detect_dominant_language(Text=text)
    return response
