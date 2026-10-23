import json

from identity_client import cognito_idp_client, load_identity_config
from identity_models import RegisterUserRequest, normalize_email, to_payload


def register_user(email: str, password: str, locale: str = None, display_name: str = None):
    config = load_identity_config()
    client = cognito_idp_client()
    payload = to_payload(
        RegisterUserRequest(
            email=normalize_email(email),
            password=password,
            locale=locale,
            display_name=display_name,
        )
    )
    attributes = [{"Name": "email", "Value": payload["email"]}]
    if payload.get("locale"):
        attributes.append({"Name": "locale", "Value": payload["locale"]})
    if payload.get("display_name"):
        attributes.append({"Name": "name", "Value": payload["display_name"]})
    response = client.sign_up(
        ClientId=config.client_id,
        Username=payload["email"],
        Password=payload["password"],
        UserAttributes=attributes,
    )
    return {"user_sub": response.get("UserSub"), "user_confirmed": response.get("UserConfirmed", False)}


def lambda_handler(event, context):
    body = event if isinstance(event, dict) else json.loads(event)
    return register_user(body["email"], body["password"], body.get("locale"), body.get("display_name"))
