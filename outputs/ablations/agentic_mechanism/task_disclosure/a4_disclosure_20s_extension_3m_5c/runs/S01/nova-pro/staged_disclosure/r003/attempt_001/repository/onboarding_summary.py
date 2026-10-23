import zenpy
from zenpy import Zenpy

def summarize_onboarding_state():
    credentials = {
        'email': 'your_email@example.com',
        'api_token': 'your_api_token',
        'subdomain': 'your_subdomain'
    }
    zenpy_client = Zenpy(**credentials)
    tickets = zenpy_client.search(type='ticket', tags='onboarding')
    summary = {
        'total_tickets': len(tickets),
        'open_tickets': sum(1 for ticket in tickets if ticket.status == 'open'),
        'closed_tickets': sum(1 for ticket in tickets if ticket.status == 'closed')
    }
    return summary

if __name__ == '__main__':
    onboarding_summary = summarize_onboarding_state()
    print(onboarding_summary)