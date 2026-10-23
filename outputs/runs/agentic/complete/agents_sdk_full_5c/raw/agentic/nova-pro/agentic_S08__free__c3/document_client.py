import os
import boto3

os.environ['AWS_PROFILE'] = 'default'

textract = boto3.client('textract')
comprehend = boto3.client('comprehend')
translate = boto3.client('translate')
dynamodb = boto3
.resource('dynamodb')

def get_textract_client():
    return textract

def get_comprehend_client():
    return comprehend

def get_translate_client():
    return translate

def get_dynamodb_resource():
    return dynamodb