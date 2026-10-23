import os
from openai import OpenAI
from security_models import EncryptionResponse, DecryptionResponse, SignResponse, VerifyResponse


def generate_crypto_audit_embedding(event: dict) -> list:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    event_type = event.get("event_type", "unknown")
    event_data = event.get("data", {})
    
    prompt = f"Generate a concise audit note for a {event_type} event: {event_data}"
    
    response = client.embeddings.create(
        input=prompt,
        model="text-embedding-ada-002"
    )
    
    return response.data[0].embedding


def create_encryption_event(response: EncryptionResponse) -> dict:
    return {
        "event_type": "encryption",
        "data": {
            "key_id": response.key_id,
            "algorithm": response.algorithm
        }
    }


def create_decryption_event(response: DecryptionResponse) -> dict:
    return {
        "event_type": "decryption",
        "data": {
            "key_id": response.key_id,
            "algorithm": response.algorithm
        }
    }


def create_sign_event(response: SignResponse) -> dict:
    return {
        "event_type": "sign",
        "data": {
            "key_id": response.key_id,
            "algorithm": response.algorithm
        }
    }


def create_verify_event(response: VerifyResponse) -> dict:
    return {
        "event_type": "verify",
        "data": {
            "key_id": response.key_id,
            "algorithm": response.algorithm,
            "is_valid": response.is_valid
        }
    }