import os
import json
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import boto3
from botocore.exceptions import ClientError


def envelope_encrypt(plaintext: str, key_id: str = None) -> dict:
    """
    Implement envelope encryption using AWS KMS managed key.

    Args:
        plaintext: The plaintext to encrypt
        key_id: Optional AWS KMS key ID. If not provided, uses default key.

    Returns:
        Dictionary with envelope encryption data
    """
    # Initialize AWS KMS client
    kms_client = boto3.client(
        "kms", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    # Use default key if not specified
    if not key_id:
        key_id = os.environ.get("AWS_KMS_KEY_ID", "alias/aws/envelope-key")

    try:
        # Step 1: Generate a data encryption key (DEK) from KMS
        dek_response = kms_client.generate_data_key(KeyId=key_id, KeySpec="AES_256")

        plaintext_dek = dek_response["Plaintext"]
        encrypted_dek = dek_response["CiphertextBlob"]

        # Step 2: Generate a random IV for data encryption
        iv = os.urandom(16)

        # Step 3: Encrypt the data with the DEK using AES-GCM
        cipher = Cipher(
            algorithms.AES(plaintext_dek), modes.GCM(iv), backend=default_backend()
        )

        encryptor = cipher.encryptor()

        # Add additional authenticated data (AAD) for integrity
        aad = b"envelope-encryption-v1"
        encryptor.authenticate_additional_data(aad)

        # Encrypt the plaintext
        ciphertext = encryptor.update(plaintext.encode("utf-8")) + encryptor.finalize()
        tag = encryptor.tag

        # Step 4: Prepare envelope
        envelope = {
            "version": "1.0",
            "key_id": key_id,
            "encrypted_dek": base64.b64encode(encrypted_dek).decode("utf-8"),
            "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
            "iv": base64.b64encode(iv).decode("utf-8"),
            "tag": base64.b64encode(tag).decode("utf-8"),
            "aad": base64.b64encode(aad).decode("utf-8"),
            "algorithm": "AES-256-GCM",
            "key_wrapping": "AWS-KMS",
            "provider": "aws_kms",
        }

        # Step 5: Optionally encrypt metadata with KMS
        metadata = {
            "timestamp": os.environ.get("ENCRYPTION_TIMESTAMP", ""),
            "purpose": "envelope-encryption",
            "data_size": len(plaintext),
        }

        metadata_json = json.dumps(metadata)
        metadata_encrypted = kms_client.encrypt(
            KeyId=key_id, Plaintext=metadata_json.encode("utf-8")
        )

        envelope["encrypted_metadata"] = base64.b64encode(
            metadata_encrypted["CiphertextBlob"]
        ).decode("utf-8")

        return envelope

    except ClientError as e:
        raise Exception(f"AWS KMS envelope encryption failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Envelope encryption failed: {str(e)}")


def envelope_decrypt(envelope: dict) -> str:
    """
    Decrypt envelope encrypted data using AWS KMS.

    Args:
        envelope: Envelope encryption data dictionary

    Returns:
        Decrypted plaintext string
    """
    # Initialize AWS KMS client
    kms_client = boto3.client(
        "kms", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        # Decode base64 fields
        encrypted_dek = base64.b64decode(envelope["encrypted_dek"])
        ciphertext = base64.b64decode(envelope["ciphertext"])
        iv = base64.b64decode(envelope["iv"])
        tag = base64.b64decode(envelope["tag"])
        aad = base64.b64decode(envelope["aad"])

        # Get key_id from envelope
        key_id = envelope["key_id"]

        # Step 1: Decrypt the DEK using KMS
        dek_response = kms_client.decrypt(CiphertextBlob=encrypted_dek, KeyId=key_id)

        plaintext_dek = dek_response["Plaintext"]

        # Step 2: Decrypt the data with the DEK
        cipher = Cipher(
            algorithms.AES(plaintext_dek), modes.GCM(iv, tag), backend=default_backend()
        )

        decryptor = cipher.decryptor()
        decryptor.authenticate_additional_data(aad)

        # Decrypt the ciphertext
        plaintext_bytes = decryptor.update(ciphertext) + decryptor.finalize()

        # Convert to string
        plaintext = plaintext_bytes.decode("utf-8")

        return plaintext

    except KeyError as e:
        raise Exception(f"Missing required field in envelope: {str(e)}")
    except ClientError as e:
        raise Exception(f"AWS KMS envelope decryption failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Envelope decryption failed: {str(e)}")
