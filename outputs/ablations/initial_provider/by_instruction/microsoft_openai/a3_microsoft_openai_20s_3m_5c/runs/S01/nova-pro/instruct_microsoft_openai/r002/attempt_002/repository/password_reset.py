import requests

def password_reset(email):
    url = 'https://graph.microsoft.com/v1.0/users/{email}/sendPasswordResetMail'
    headers = {
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN'
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 202:
        return 'Password reset email sent'
    else:
        return 'Failed to send password reset email'