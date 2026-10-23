import os
import requests

def check_annotation_safety(annotation):
    response = requests.post(
        'https://api.perspectiveapi.com/v1/comment',
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {os.getenv(