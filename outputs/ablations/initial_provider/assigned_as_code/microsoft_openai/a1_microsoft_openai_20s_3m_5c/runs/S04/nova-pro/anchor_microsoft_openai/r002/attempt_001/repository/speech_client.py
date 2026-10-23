import os
import requests

def create_client(region, api_key=None):
    api_key = api_key or os.environ.get('AZURE_SPEECH_KEY')
    return {'region': region, 'api_key': api_key}