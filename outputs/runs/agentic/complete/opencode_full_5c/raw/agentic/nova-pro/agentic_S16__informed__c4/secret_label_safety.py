import requests

def check_unsafe_text(text):
    url = 'https://api.tisane.ai/v1/moderation'
    headers = {'Authorization': f'Bearer {os.getenv(