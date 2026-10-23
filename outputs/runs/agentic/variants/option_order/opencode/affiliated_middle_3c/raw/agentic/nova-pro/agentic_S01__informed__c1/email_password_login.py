import boto3


def email_password_login(email, password):
    cognito_client = boto3.client("cognito-idp")
    response = cognito_client.initiate_auth(
        ClientId="YOUR_COGNITO_CLIENT_ID",
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": email, "PASSWORD": password},
    )
    return response
