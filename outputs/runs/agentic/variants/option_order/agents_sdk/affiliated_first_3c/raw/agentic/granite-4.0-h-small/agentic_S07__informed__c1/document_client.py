import os
import base64

# Minimal helpers to load images and create Textract client

def load_image_bytes(image_path):
    '''Load a local image file and return raw bytes.'''
    with open(image_path, 'rb') as f:
        return f.read()

def get_textract_client():
    '''Helper to create a boto3 Textract client using environment credentials.'''
    # AWS SDK will automatically pick up credentials from environment variables.
    # Ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set.
    import boto3
    return boto3.client('textract')
