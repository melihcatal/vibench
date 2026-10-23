import os
import requests
from identity_client import IBMAppIDClient
from identity_models import LoginRequest, LoginResponse, normalize_login_response


def email_password_login(email: str, password: str) -> LoginResponse:
    client = IBMAppIDClient()
    return client.email_password_login(LoginRequest(email=email, password=password))
