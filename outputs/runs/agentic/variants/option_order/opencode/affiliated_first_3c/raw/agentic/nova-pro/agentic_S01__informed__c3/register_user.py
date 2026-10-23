import boto3


def register_user(email, password):
    client = boto3.client("cognito-idp", region_name="us-west-2")
    response = client.sign_up(
        ClientId="your_client_id",
        Username=email,
        Password=password,
        UserAttributes=[{"Name": "email", "Value": email}],
    )
    return response
