import os
import boto3

def check_corpus_safety(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(Text=text)
    return response