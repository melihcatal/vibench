import requests

AUTH0_DOMAIN = 'your-auth0-domain.auth0.com'
MANAGEMENT_API_TOKEN = 'your-management-api-token'

def start_password_reset(email):
    url = f'https://{AUTH0_DOMAIN}/api/v2/jobs/email-password-change'
    headers = {
        'Authorization': f'Bearer {MANAGEMENT_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'client_id': 'your-client-id',
        'connection': 'your-connection-name',
        'email': email
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':\n    email = 'user@example.com'\n    print(start_password_reset(email))