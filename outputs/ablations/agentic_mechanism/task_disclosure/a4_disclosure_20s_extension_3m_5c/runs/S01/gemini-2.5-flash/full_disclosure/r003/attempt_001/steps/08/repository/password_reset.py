
import os
import requests
import json

class PasswordReset:
    def __init__(self, domain, client_id):
        self.domain = domain
        self.client_id = client_id
        self.url = f"https://{self.domain}/dbconnections/change_password"

    def start_password_reset(self, email, connection="Username-Password-Authentication"):
        headers = {'Content-Type': 'application/json'}
        payload = {
            'client_id': self.client_id,
            'email': email,
            'connection': connection
        }
        try:
            response = requests.post(self.url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            return {"status": "success", "message": response.text}
        except requests.exceptions.HTTPError as err:
            return {"status": "error", "message": str(err), "details": response.json()}
        except requests.exceptions.RequestException as err:
            return {"status": "error", "message": str(err)}

if __name__ == '__main__':
    # Replace with your Auth0 domain and client ID
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN.auth0.com")
    AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID")

    # Example Usage:
    # password_reset_client = PasswordReset(AUTH0_DOMAIN, AUTH0_CLIENT_ID)
    # email_to_reset = "user@example.com" # Replace with a valid user email
    # result = password_reset_client.start_password_reset(email_to_reset)
    # print(result)
