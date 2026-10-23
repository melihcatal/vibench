from identity_client import identity_client
from identity_models import UserRegistration

def register_user(user_reg: UserRegistration) -> str:
    try:
        user = identity_client.auth_sdk.create_user(
            email=user_reg.email,
            password=user_reg.password
        )
        return user.uid
    except Exception as e:
        raise RuntimeError(f"Failed to register user: {e}")
