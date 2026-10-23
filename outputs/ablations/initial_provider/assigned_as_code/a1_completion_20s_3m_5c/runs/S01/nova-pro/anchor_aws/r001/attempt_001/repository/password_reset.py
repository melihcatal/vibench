import boto3

def password_reset(email, config=None):
    config = config or {}
    client = boto3.client('cognito-idp', region_name=config.get('region'))
    response = client.forgot_password(
        ClientId=config['client_id'],
        Username=email
    )
    return {'code_delivery_details': response['CodeDeliveryDetails']}
