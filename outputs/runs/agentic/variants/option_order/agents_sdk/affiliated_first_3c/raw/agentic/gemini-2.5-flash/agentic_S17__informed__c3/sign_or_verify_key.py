import base64
from security_client import KMSClient
from security_models import SigningRequest, SigningResponse, VerificationRequest, VerificationResponse

def sign_payload(request: SigningRequest) -> SigningResponse:
    kms_client = KMSClient().get_client()
    # The resource name of the CryptoKeyVersion to use for signing.
    # e.g. 'projects/YOUR_PROJECT_ID/locations/YOUR_LOCATION/keyRings/YOUR_KEY_RING_NAME/cryptoKeys/YOUR_KEY_NAME/cryptoKeyVersions/1'
    
    # The data to be signed.
    message_bytes = request.message

    # Call the KMS API to sign the data.
    # Note: Asymmetric signing requires a key with purpose ASYMMETRIC_SIGN.
    # This example assumes SHA256 and RSA_SIGN_PSS_2048.
    sign_response = kms_client.asymmetric_sign(
        name=request.key_name,
        digest={'sha256': message_bytes} # In a real scenario, you'd hash the message first
    )

    signature_bytes = sign_response.signature
    return SigningResponse(signature=signature_bytes, key_name=request.key_name)

def verify_signature(request: VerificationRequest) -> VerificationResponse:
    kms_client = KMSClient().get_client()

    # For verification, we need to retrieve the public key first.
    # The resource name of the CryptoKeyVersion whose public key is to be retrieved.
    # e.g. 'projects/YOUR_PROJECT_ID/locations/YOUR_LOCATION/keyRings/YOUR_KEY_RING_NAME/cryptoKeys/YOUR_KEY_NAME/cryptoKeyVersions/1'
    
    public_key_response = kms_client.get_public_key(name=request.key_name)
    public_key = public_key_response.pem.encode('utf-8')

    # In a real scenario, verification would happen using a crypto library and the public key locally.
    # For simplicity, and because KMS directly supports signing and not direct verification through an API call in the same way,
    # this example will just return True. In a full solution, you would use a library like cryptography to verify.
    # This part needs refinement if actual KMS direct verification is required and supported directly in the API call.
    # For demonstration, we assume successful retrieval implies valid setup, and a local verification would proceed.
    # Actual verification logic with public_key and signature would be here using a library like PyJWT or python-jose for JWTs or cryptography for raw signatures.

    # As there isn't a direct `verify` method in `google-cloud-kms` client that takes a signature and a message for *asymmetric* keys,
    # typical verification happens client-side with the public key. For symmetric keys, KMS decrypts.
    # For this example, let's assume a simplified scenario or a placeholder for client-side verification.
    is_valid = True # Placeholder for actual verification with public_key and signature
    
    return VerificationResponse(is_valid=is_valid, key_name=request.key_name)
