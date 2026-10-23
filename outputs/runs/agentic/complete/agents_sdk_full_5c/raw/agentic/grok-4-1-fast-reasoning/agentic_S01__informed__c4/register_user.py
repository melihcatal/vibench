from identity_client import get_cognito_client
from identity_models import build_register_payload, build_set_password_payload

def register_user(email: str, password: str):
    client = get_cognito_client()
    create_payload = build_register_payload(email, password)
    user = client.admin_create_user(**create_payload)
    set_payload = build_set_password_payload(email, password)
    client.admin_set_user_password(**set_payload)
    return {"status": "success", "user_sub": user["User"]["Username"]}