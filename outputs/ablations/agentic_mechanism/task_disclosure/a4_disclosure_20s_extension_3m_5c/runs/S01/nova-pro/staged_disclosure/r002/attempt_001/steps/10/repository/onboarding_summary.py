import requests

ZENDESK_SUBDOMAIN = 'your_subdomain'
ZENDESK_EMAIL = 'your_email'
ZENDESK_TOKEN = 'your_token'

def get_onboarding_state():
    url = f'https://{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2/users/me'
    auth = (f'{ZENDESK_EMAIL}/token', ZENDESK_TOKEN)
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    user_data = response.json()
    onboarding_state = user_data['user']['tags']
    return onboarding_state

if __name__ == '__main__':
    onboarding_state = get_onboarding_state()
    print(f'Onboarding state: {onboarding_state}')
