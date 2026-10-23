import os
import requests

API_KEY = os.getenv('PERSPECTIVE_API_KEY')
ANALYZE_URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'

def check_script(script_path):
    with open(script_path, 'r') as file:
        script_content = file.read()
    payload = {
        'comment': {'text': script_content},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    response = requests.post(ANALYZE_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Failed to analyze script')

if __name__ == '__main__':
    script_path = 'example_script.txt'
    result = check_script(script_path)
    print(result)