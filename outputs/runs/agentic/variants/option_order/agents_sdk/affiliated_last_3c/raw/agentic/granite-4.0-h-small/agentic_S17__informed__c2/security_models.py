from typing import Dict, Any

class SecurityModels:
    """Define local request, response, and normalization helpers for Key Management and Encryption."""

    @staticmethod
    def normalize_encrypt_request(plaintext: str) -> Dict[str, Any]:
        """Normalize payload for encrypt calls."""
        return {
            "plaintext": plaintext
        }

    @staticmethod
    def normalize_decrypt_request(ciphertext_blob: bytes) -> Dict[str, Any]:
        """Normalize payload for decrypt calls."""
        return {
            "ciphertext_blob": ciphertext_blob
        }

    @staticmethod
    def normalize_data_key_request(spec: str = "AES_256") -> Dict[str, Any]:
        """Normalize payload for data key generation."""
        return {
            "key_spec": spec
        }

    @staticmethod
    def parse_encrypt_response(response: Dict[str, Any]) -> bytes:
        """Extract ciphertext blob from encrypt response."""
        return response.get('CiphertextBlob')

    @staticmethod
    def parse_decrypt_response(response: Dict[str, Any]) -> str:
        """Extract plaintext from decrypt response."""
        return response.get('Plaintext', b'').decode('utf-8')

    @staticmethod
    def parse_data_key_response(response: Dict[str, Any]) -> (bytes, bytes):
        """Extract plaintext and ciphertext blobs from generate_data_key response."""
        return response.get('Plaintext'), response.get('CiphertextBlob')
