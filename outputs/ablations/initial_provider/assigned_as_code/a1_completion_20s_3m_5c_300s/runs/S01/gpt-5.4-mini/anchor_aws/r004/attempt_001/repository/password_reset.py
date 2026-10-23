import boto3

from identity_client import ensure_identity_config, secret_hash
from identity_models import build_cognito_username


def password_reset(payload, config=None):
    config = ensure_identity_config(config, required=("client_id",))
    client = boto3.client("cognito-idp", region_name=config.get("region"))
    username = build_cognito_username(payload)
    request = {"ClientId": config["client_id"], "Username": username}
    sh = secret_hash(username, config["client_id"], config.get("client_secret"))
    if sh:
        request["SecretHash"] = sh
    response = client.forgot_password(**request)
    code_delivery = response.get("CodeDeliveryDetails", {})
    return {"delivery_destination": code_delivery.get("Destination"), "delivery_medium": code_delivery.get("DeliveryMedium")}
