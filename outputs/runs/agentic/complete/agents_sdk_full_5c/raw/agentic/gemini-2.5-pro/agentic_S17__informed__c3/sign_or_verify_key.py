from security_client import SecurityClient
from security_models import SigningRequest, SigningResponse

def sign_with_managed_key(request: SigningRequest) -> SigningResponse:
    """
    Signs a message using an asymmetric key managed by AWS KMS.
    
    Note: For `MessageType='RAW'`, the message is limited to 4096 bytes.
    For larger messages, you should create a hash digest of the message
    and pass that as the message with `MessageType='DIGEST'`.
    """
    kms_client = SecurityClient.get_kms_client()
    
    response = kms_client.sign(
        KeyId=request.key_id,
        Message=request.message,
        MessageType='RAW',
        SigningAlgorithm=request.signing_algorithm
    )
    
    return SigningResponse(
        signature=response['Signature'],
        key_id=response['KeyId']
    )
