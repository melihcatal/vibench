from identity_client import get_stytch_client
from identity_models import RegisterRequest, RegisterResponse


def register_user(request: RegisterRequest) -> RegisterResponse:
    client = get_stytch_client()
    result = client.email.passwords.create(
        email=request.email, password=request.password
    )
    user = result.user
    email = user.email_addresses[0].email if user.email_addresses else request.email
    return RegisterResponse(user_id=user.id, email=email)
