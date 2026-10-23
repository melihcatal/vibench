import os
from identity_client import create_cognito_client, get_app_client_id
from identity_models import build_user_attributes

def register_user(email: str, password: str, **extra_attrs) -&gt; dict:
    client = create_cognito_client()
    client_id = get_app_client_id()
    resp = client.sign_up(
        ClientId=client_id,
        Username=email.lower(),
        Password=password,
        UserAttributes=build_user_attributes(email, **extra_attrs),
    )
    return {
        'user_sub': resp['UserSub'],
        'user_confirmed': resp['UserConfirmed'],
        'code_delivery_details': resp.get('CodeDeliveryDetails'),
    }