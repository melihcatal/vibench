import boto3

from identity_client import (
    app_client_id,
    cognito_client,
    normalize_name,
    user_pool_id,
    config_value,
)
from identity_models import EmailPasswordRegistration, response_payload


def register_user(
    email: str, password: str, locale: str = "en", display_name: str | None = None
):
    req = EmailPasswordRegistration(
        email=email, password=password, locale=locale, display_name=display_name
    ).normalized()
    client = cognito_client()
    attrs = [{"Name": "email", "Value": req["email"]}]
    if req["display_name"]:
        attrs.append({"Name": "name", "Value": normalize_name(req["display_name"])})
    result = client.sign_up(
        ClientId=app_client_id(),
        Username=req["email"],
        Password=req["password"],
        UserAttributes=attrs,
        ValidationData=[{"Name": "locale", "Value": req["locale"]}],
    )
    return response_payload(
        "Amazon Cognito User Pools",
        "register_user",
        {
            "user_sub": result.get("UserSub"),
            "confirmed": result.get("UserConfirmed", False),
        },
    )
