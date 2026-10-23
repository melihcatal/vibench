import os
from identity_client import IBMAppIDClient
from identity_models import RegisterRequest, RegisterResponse


def register_user(email: str, password: str) -> RegisterResponse:
    client = IBMAppIDClient()
    request = RegisterRequest(email=email, password=password)
    return client.register_user(request)
