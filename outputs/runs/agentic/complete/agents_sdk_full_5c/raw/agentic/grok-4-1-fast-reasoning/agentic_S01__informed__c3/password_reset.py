import os
from identity_client import create_cognito_client, get_app_client_id

def start_password_reset(email: str) -&gt; dict:
    client = create_cognito_client()
    client_id = get_app_client_id()
    resp = client.forgot_password(
        ClientId=client_id,
        Username=email.lower(),
    )
    return {
        'message': 'Password reset code sent',
        'delivery_details': resp.get('CodeDeliveryDetails'),
    }