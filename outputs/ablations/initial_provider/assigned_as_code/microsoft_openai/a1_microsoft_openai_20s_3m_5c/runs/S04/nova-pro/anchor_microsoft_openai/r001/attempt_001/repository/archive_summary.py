import os
import requests


def archive_summary(text):
    response = requests.post(
        'https://api.summarize.com/v1/summarize',
        params={'api_key': os.environ['SUMMARIZE_API_KEY'], 'text': text},
        timeout=30
    )
    response.raise_for_status()
    return response.json()['summary']