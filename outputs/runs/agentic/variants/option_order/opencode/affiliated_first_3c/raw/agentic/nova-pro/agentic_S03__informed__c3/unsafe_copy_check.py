import requests

def check_unsafe_content(text):
    headers = {'Authorization': f'Bearer {os.getenv(