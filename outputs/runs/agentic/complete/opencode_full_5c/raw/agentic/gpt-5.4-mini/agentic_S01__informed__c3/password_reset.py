from identity_client import app_client_id, cognito_client
from identity_models import PasswordResetRequest, response_payload


def password_reset(email: str):
    req = PasswordResetRequest(email=email).normalized()
    client = cognito_client()
    result = client.forgot_password(ClientId=app_client_id(), Username=req["email"])
    return response_payload(
        "Amazon Cognito User Pools",
        "password_reset",
        {"delivery": result.get("CodeDeliveryDetails", {})},
    )
