import os
import requests
from identity_client import Auth0Client
from identity_models import PasswordResetRequest, PasswordResetResponse


class PasswordResetInitiator:
    def __init__(self):
        self.client = Auth0Client()

    def initiate_password_reset(self, request: PasswordResetRequest) -> PasswordResetResponse:
        url = f"https://{self.client.domain}/dbconnections/change_password"
        payload = {
            "client_id": self.client.client_id,
            "email": request["email"],
            "connection": self.client.connection,
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return self.client._normalize_password_reset_response("reset_email_sent")