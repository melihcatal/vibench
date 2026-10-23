import boto3
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse

def sign_payload(request: SignRequest) -> SignResponse:
    client = boto3.client("kms", region_name=request.region)
    response = client.sign(
        KeyId=request.key_id,
        Message=request.message,
        MessageType='RAW',
        SigningAlgorithm=request.signing_algorithm
    )
    return SignResponse(
        signature=response["Signature"],
        key_id=request.key_id,
        region=request.region,
        signing_algorithm=request.signing_algorithm
    )

def verify_signature(request: VerifyRequest) -> VerifyResponse:
    client = boto3.client("kms", region_name=request.region)
    response = client.verify(
        KeyId=request.key_id,
        Message=request.message,
        MessageType='RAW',
        Signature=request.signature,
        SigningAlgorithm=request.signing_algorithm
    )
    return VerifyResponse(
        signature_valid=response["SignatureValid"],
        key_id=request.key_id,
        region=request.region
    )
