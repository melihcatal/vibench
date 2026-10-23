import requests

ZEN_DOMAIN = 'your_zendesk_domain'
API_TOKEN = 'your_api_token'

def get_onboarding_tickets():
    url = f'https://{ZEN_DOMAIN}.zendesk.com/api/v2/search.json'
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    params = {
        'query': 'type:ticket tags:onboarding'
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def summarize_onboarding_state():
    tickets = get_onboarding_tickets()
    summary = {
        'total': len(tickets['results']),
        'open': sum(1 for ticket in tickets['results'] if ticket['status'] == 'open'),
        'closed': sum(1 for ticket in tickets['results'] if ticket['status'] == 'closed')
    }
    return summary

if __name__ == '__main__':\n    summary = summarize_onboarding_state()
    print(f'Onboarding Summary: {summary}')
