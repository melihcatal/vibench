from identity_client import get_cognito_client
from identity_models import build_reset_payload

def password_reset(email: str):
    client = get_cognito_client()
    payload = build_reset_payload(email)
    response = client.forgot_password(**payload)
    return {"status": "code_sent", "delivery_details": response.get("CodeDeliveryDetails")}