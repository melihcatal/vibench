from identity_client import get_identity_client, get_client_id
from identity_models import PasswordResetRequest

def initiate_password_reset(reset_request: PasswordResetRequest) -> str:
    """
    Initiates a password reset flow for a user in Amazon Cognito.
    """
    client = get_identity_client()
    client_id = get_client_id()
    
    response = client.forgot_password(
        ClientId=client_id,
        Username=reset_request.email
    )
    
    # The destination (e.g., email) where the code was sent
    return response['CodeDeliveryDetails']['Destination']
