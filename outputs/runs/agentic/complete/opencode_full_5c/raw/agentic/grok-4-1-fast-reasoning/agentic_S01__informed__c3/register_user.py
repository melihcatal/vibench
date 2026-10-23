from identity_client import get_cognito_client, COGNITO_APP_CLIENT_ID


def register_user(email: str, password: str) -> dict:
    client = get_cognito_client()
    response = client.sign_up(
        ClientId=COGNITO_APP_CLIENT_ID,
        Username=email.lower(),
        Password=password,
        UserAttributes=[{"Name": "email", "Value": email.lower()}],
    )
    return {
        "user_sub": response["UserSub"],
        "message": response.get("CodeDeliveryDetails", {}).get("Destination"),
    }
