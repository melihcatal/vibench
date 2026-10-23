from identity_client import IdentityClient
from identity_models import RegisterUserRequest, RegisterUserResponse

def register_user(request: RegisterUserRequest) -> RegisterUserResponse:
    client = IdentityClient()
    auth = client.get_auth_client()

    try:
        user = auth.create_user(
            email=request.email,
            password=request.password
        )
        return RegisterUserResponse(uid=user.uid, email=user.email, display_name=user.display_name)
    except Exception as e:
        # In a real application, you would handle different Firebase Auth exceptions
        # more gracefully (e.g., email already exists, weak password).
        print(f"Error registering user: {e}")
        raise
