from identity_client import get_identity_client, get_identity_settings
from identity_models import RegisterUserRequest, normalize_user_record


def register_user(email: str, password: str, display_name: str | None = None, locale: str | None = None) -> dict:
    settings = get_identity_settings()
    client = get_identity_client()
    payload = RegisterUserRequest(email=email, password=password, display_name=display_name, locale=locale).to_payload()
    result = client.users.sign_up(
        email=payload["email"],
        password=payload["password"],
        options={
            "data": payload["metadata"],
        },
    )
    return normalize_user_record(result.user, settings.provider)
