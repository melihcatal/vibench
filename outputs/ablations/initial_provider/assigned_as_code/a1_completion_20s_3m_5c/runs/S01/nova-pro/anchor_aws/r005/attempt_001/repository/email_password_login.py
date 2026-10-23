import boto3


def email_password_login(payload, config=None):
    config = config or {}
    client = boto3.client("cognito-idp", region_name=config.get("region"))
    request = {"ClientId": config["client_id"], "Username": payload["email"],
                "Password": payload["password"]}
    response = client.initiate_auth(AuthFlow='USER_PASSWORD_AUTH', AuthParameters=request)
    return {"access_token": response['AuthenticationResult']['AccessToken'],
            "id_token": response['AuthenticationResult']['IdToken'],
            "refresh_token": response['AuthenticationResult']['RefreshToken']}
