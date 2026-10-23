import os
import re
from google.cloud import kms_v1
from security_client import KmsClient

# Reuse the consolidated decryption helper that also records usage and safety
from key_usage_summary import _record_usage, is_payload_safe

# Central handler that fetches, decrypts, validates, and normalizes a payload.
# It returns the plaintext if safe, raises a custom exception otherwise.

class PayloadSafety:
    @staticmethod
    def fetch_and_validate(cipher_b64: str, key_name: str) -> str:
        """
        Parameters
        ----------
        cipher_b64 : str
            Base64-encoded ciphertext produced by a KMS encryption call.
        key_name : str
            Full resource name of the KMS crypto key to use for decryption.

        Returns
        -------
        str
            The plaintext after decryption and basic safety checks.
        """
        # 1. Decode the incoming ciphertext
        ciphertext = base64.b64decode(cipher_b64)
        
        # 2. Decrypt using the KMS client (also records usage)
        try:
            decrypt_resp = KmsClient().decrypt(key_name, ciphertext)
        except Exception as exc:
            raise RuntimeError(f"KMS decryption failed: {exc}") from exc
        
        # 3. Record usage counter
        _record_usage(\"DECRYPT\")
        
        # 4. Convert decrypted bytes to string, stripping PKCS7 padding if present
        try:
            plaintext = decrypt_resp.plaintext.decode('utf-8')
        except UnicodeDecodeError as ue:
            raise ValueError(f"Decrypted data is not valid UTF-8: {ue}") from ue
        
        # 5. Perform basic safety/content check before returning
        if not is_payload_safe(plaintext):
            raise ValueError("Payload failed safety validation (contains unsafe patterns).")
        
        return plaintext
