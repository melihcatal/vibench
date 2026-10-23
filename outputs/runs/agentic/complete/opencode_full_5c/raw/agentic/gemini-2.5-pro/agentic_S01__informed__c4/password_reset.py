from identity_client import get_identity_client, get_app_client_id


def request_password_reset(email: str) -> str:
    client = get_identity_client()
    app_client_id = get_app_client_id()

    response = client.forgot_password(ClientId=app_client_id, Username=email)
    return response["CodeDeliveryDetails"]["Destination"]
