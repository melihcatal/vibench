import os
import requests


def moderate_vendor_text(text):
    response = requests.post(os.getenv('TEXT_MODERATION_ENDPOINT'), json={'text': text})
    if response.status_code!= 200:
        raise Exception('Text moderation service error')
    result = response.json()
    if result.get('flagged'):
        raise ValueError('Vendor text contains inappropriate content')