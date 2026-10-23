from identity_client import get_cognito_client, COGNITO_CLIENT_ID


def password_reset(email: str) -> dict:
    client = get_cognito_client()
    resp = client.forgot_password(ClientId=COGNITO_CLIENT_ID, Username=email)
    return {
        "message": "Password reset code sent",
        "code_delivery_details": resp.get("CodeDeliveryDetails", {}),
    }
