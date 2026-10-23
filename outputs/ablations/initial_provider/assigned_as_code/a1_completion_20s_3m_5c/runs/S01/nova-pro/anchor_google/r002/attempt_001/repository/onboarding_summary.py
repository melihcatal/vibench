import os
import requests


def summarize_onboarding_state(user_id):
    api_key = os.getenv('SUMMARIZE_API_KEY')
    url = f'https://api.summarize.com/summarize?key={api_key}'
    response = requests.post(url, json={"text": f'Onboarding state for user {user_id}.'})
    return response.json()['summary']
