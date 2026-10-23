import requests

def password_reset(email, config=None):
    config = config or {}
    response = requests.post(f"https://graph.microsoft.com/v1.0/users/{email}/sendPasswordResetMail", headers={'Authorization': 'Bearer ' + config['access_token']})
    response.raise_for_status()
    return {'status': 'password reset email sent'}
