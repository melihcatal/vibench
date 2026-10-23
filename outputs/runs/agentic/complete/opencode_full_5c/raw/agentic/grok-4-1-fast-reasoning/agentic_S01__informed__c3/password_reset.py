from identity_client import get_cognito_client, COGNITO_APP_CLIENT_ID


def password_reset(email: str) -> dict:
    client = get_cognito_client()
    response = client.forgot_password(
        ClientId=COGNITO_APP_CLIENT_ID, Username=email.lower()
    )
    return {
        "message_action": response.get("MessageAction"),
        "destination": response.get("CodeDeliveryDetails", {}).get("Destination"),
    }
