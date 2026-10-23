from identity_client import CognitoIdentityClient

def register_user(email: str, password: str) -> dict:
    client = CognitoIdentityClient()
    response = client.client.sign_up(
        ClientId=client.app_client_id,
        Username=email,
        Password=password,
        UserAttributes=[
            {
                'Name': 'email',
                'Value': email
            }
        ]
    )
    return {
        'user_sub': response['UserSub'],
        'code_delivery_details': response.get('CodeDeliveryDetails')
    }