import os
from identity_client import IdentityClient
from identity_models import RegisterRequest, RegisterResponse


def register_user(email: str, password: str) -> RegisterResponse:
    client = IdentityClient()
    request = RegisterRequest(email=email, password=password)
    return client.register_user(request)


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 3:
        email, password = sys.argv[1], sys.argv[2]
        response = register_user(email, password)
        print(f"User registered: {response.user_id}")
