import os
from openai import OpenAI
from security_client import get_openai_client

def sign_payload(payload: str, signing_key_id: str) -> str:
    """
    Signs a payload using OpenAI to simulate a managed key service for signing.
    In a real scenario, this would involve a KMS key for digital signing.
    """
    client = get_openai_client()
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Using a concrete model identifier
            messages=[
                {"role": "system", "content": "You are a signing service. Sign the following payload."},
                {"role": "user", "content": f"Sign with key {signing_key_id}: {payload}"}
            ]
        )
        signature = response.choices[0].message.content.encode('utf-8').hex()
        return signature
    except Exception as e:
        return f"Signing failed: {e}"

def verify_payload(payload: str, signature: str, signing_key_id: str) -> bool:
    """
    Verifies a payload and signature using OpenAI to simulate a managed key service for verification.
    In a real scenario, this would involve a KMS key for digital signature verification.
    """
    client = get_openai_client()

    try:
        decoded_signature = bytes.fromhex(signature).decode('utf-8', errors='ignore')
        response = client.chat.completions.create(
            model="gpt-4o",  # Using a concrete model identifier
            messages=[
                {"role": "system", "content": "You are a verification service. Verify the following payload and signature."},
                {"role": "user", "content": f"Verify payload '{payload}' with signature '{decoded_signature}' using key {signing_key_id}"}
            ]
        )
        # For simulation, we assume if OpenAI responds positively, it's verified.
        # In a real system, there would be cryptographic verification.
        verification_result = "verified" in response.choices[0].message.content.lower()
        return verification_result
    except Exception as e:
        print(f"Verification failed: {e}")
        return False

if __name__ == '__main__':
    example_payload = "This data needs to be signed and verified."
    example_signing_key_id = "openai-signing-key-456"

    # Simulate signing
    generated_signature = sign_payload(example_payload, example_signing_key_id)
    print(f"Payload: {example_payload}")
    print(f"Generated Signature (simulated with OpenAI): {generated_signature}")

    # Simulate verification
    is_verified = verify_payload(example_payload, generated_signature, example_signing_key_id)
    print(f"Verification Result (simulated with OpenAI): {is_verified}")

    # Test with a tampered payload
    tampered_payload = "This data has been tampered with."
    is_tampered_verified = verify_payload(tampered_payload, generated_signature, example_signing_key_id)
    print(f"Verification with tampered payload: {is_tampered_verified}")
