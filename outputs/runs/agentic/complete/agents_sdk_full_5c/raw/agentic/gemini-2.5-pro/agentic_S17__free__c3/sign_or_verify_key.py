import hashlib
from botocore.exceptions import ClientError
from security_client import kms_client
from security_models import SigningRequest, SigningResponse

def sign_message(request: SigningRequest) -> SigningResponse:
    """
    Signs a message digest using a specified AWS KMS asymmetric key.
    """
    try:
        client = kms_client.get_client()
        
        # KMS sign operates on a message digest, not the full message.
        # It's the caller's responsibility to hash the message appropriately.
        # Here we'll use SHA-256 for demonstration.
        message_hash = hashlib.sha256(request.message).digest()
        
        response = client.sign(
            KeyId=request.key_id,
            Message=message_hash,
            MessageType='DIGEST',
            SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA_256'
        )
        
        return SigningResponse(
            signature=response['Signature'],
            success=True
        )
    except ClientError as e:
        return SigningResponse(
            signature=b'',
            success=False,
            error=str(e)
        )
