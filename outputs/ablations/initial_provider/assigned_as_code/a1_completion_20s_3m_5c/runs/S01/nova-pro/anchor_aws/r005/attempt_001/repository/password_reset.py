import boto3


def password_reset(email, config=None):
    config = config or {}
    client = boto3.client("cognito-idp", region_name=config.get("region"))
    request = {"ClientId": config["client_id"], "Username": email}
    response = client.forgot_password(**request)
    return {"status": response['CodeDeliveryDetails']['Destination']}
