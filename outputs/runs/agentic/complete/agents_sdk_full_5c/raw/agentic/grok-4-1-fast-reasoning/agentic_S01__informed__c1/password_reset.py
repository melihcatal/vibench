from identity_client import CognitoIdentityClient

def password_reset(email: str) -> dict:
    client = CognitoIdentityClient()
    response = client.client.forgot_password(
        ClientId=client.app_client_id,
        Username=email
    )
    return {
        'message': 'Password reset code sent to email',
        'delivery_medium': response['CodeDeliveryDetails']['DeliveryMedium'],
        'destination': response['CodeDeliveryDetails']['Destination']
    }