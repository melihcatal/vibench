import requests

def password_reset(email, config=None):
    config = config or {}
    response = requests.post('https://graph.microsoft.com/v1.0/users/' + email + '/sendPasswordReset',
        headers={'Authorization': 'Bearer ' + config['access_token']},
        json={}, timeout=30)
    response.raise_for_status()
    return {'status': 'Password reset email sent'}