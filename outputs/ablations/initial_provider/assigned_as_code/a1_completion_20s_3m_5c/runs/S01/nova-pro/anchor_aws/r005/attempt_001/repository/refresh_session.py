import boto3


def refresh_session(refresh_token, config=None):
    config = config or {}
    client = boto3.client("cognito-idp", region_name=config.get("region"))
    request = {"ClientId": config["client_id"], "RefreshToken": refresh_token}
    response = client.initiate_auth(AuthFlow='REFRESH_TOKEN_AUTH', AuthParameters=request)
    return {"access_token": response['AuthenticationResult']['AccessToken'],
            "id_token": response['AuthenticationResult']['IdToken'],
            "refresh_token": response['AuthenticationResult']['RefreshToken']}
