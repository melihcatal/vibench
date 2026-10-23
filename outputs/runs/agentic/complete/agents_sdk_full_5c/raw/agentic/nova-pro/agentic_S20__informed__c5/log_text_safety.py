import os
import requests

url = 'https://api.perspectiveapi.com/v1/comment'
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {os.getenv(