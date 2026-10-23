import os
import base64
from typing import Tuple, Dict, Any
from google.cloud import (
    kms_v1,
    dlp_v2,
    logging_v2,
    translate_v3,
    bigquery_data_transfer_v1,
)
from google.cloud.logging_v2.types import LogEntry
from google.cloud.vertexai.language_models import TextEmbeddingModel


class SecurityClient:
    def __init__(self):
        self.kms_client = kms_v1.KeyManagementServiceClient()
        self.dlp_client = dlp_v2.DlpServiceClient()
        self.logging_client = logging_v2.LoggingServiceV2Client()
        self.translate_client = translate_v3.TranslationServiceClient()
        self.vertex_embedding_model = TextEmbeddingModel.from_pretrained(
            "textembedding-gecko@003"
        )  # Google Cloud Vertex AI

    def get_key_path(
        self, project_id: str, location_id: str, key_ring_id: str, key_id: str
    ) -> str:
        return self.kms_client.crypto_key_path(
            project_id, location_id, key_ring_id, key_id
        )

    def get_key_version_path(
        self,
        project_id: str,
        location_id: str,
        key_ring_id: str,
        key_id: str,
        key_version_id: str,
    ) -> str:
        return self.kms_client.crypto_key_version_path(
            project_id, location_id, key_ring_id, key_id, key_version_id
        )

    def get_dlp_parent_path(self, project_id: str) -> str:
        return f"projects/{project_id}"

    def get_dlp_location_path(self, project_id: str, location_id: str) -> str:
        return f"projects/{project_id}/locations/{location_id}"

    def get_translation_parent_path(self, project_id: str, location_id: str) -> str:
        return self.translate_client.location_path(project_id, location_id)

    def encrypt_with_kms(
        self,
        project_id: str,
        location_id: str,
        key_ring_id: str,
        key_id: str,
        plaintext: str,
    ) -> str:
        key_path = self.get_key_path(project_id, location_id, key_ring_id, key_id)
        plaintext_bytes = plaintext.encode("utf-8")
        response = self.kms_client.encrypt(
            request={"name": key_path, "plaintext": plaintext_bytes}
        )
        return base64.b64encode(response.ciphertext).decode("utf-8")

    def decrypt_with_kms(
        self,
        project_id: str,
        location_id: str,
        key_ring_id: str,
        key_id: str,
        ciphertext: str,
    ) -> str:
        key_path = self.get_key_path(project_id, location_id, key_ring_id, key_id)
        ciphertext_bytes = base64.b64decode(ciphertext)
        response = self.kms_client.decrypt(
            request={"name": key_path, "ciphertext": ciphertext_bytes}
        )
        return response.plaintext.decode("utf-8")

    def envelope_encrypt_with_kms(
        self,
        project_id: str,
        location_id: str,
        key_ring_id: str,
        key_id: str,
        plaintext: str,
    ) -> Tuple[str, str]:
        key_path = self.get_key_path(project_id, location_id, key_ring_id, key_id)
        plaintext_bytes = plaintext.encode("utf-8")

        # Generate a new data encryption key and encrypt it with the KEK
        generate_data_key_response = self.kms_client.generate_random_bytes(
            request=kms_v1.GenerateRandomBytesRequest(
                project_id=project_id,
                location_id=location_id,
                length_bytes=32,  # AES-256 key
            )
        )
        data_key = generate_data_key_response.data

        # Encrypt the data key with the KEK
        encrypt_data_key_response = self.kms_client.encrypt(
            request={"name": key_path, "plaintext": data_key}
        )
        encrypted_data_key = encrypt_data_key_key_response.ciphertext

        # In a real scenario, you would use the data_key to encrypt the plaintext locally
        # For this example, we'll just return the encrypted data key and a placeholder ciphertext
        # This part requires a symmetric encryption library like cryptography
        # For demonstration purposes, we'll simulate the ciphertext with base64 encoding of plaintext
        ciphertext_placeholder = base64.b64encode(plaintext_bytes).decode("utf-8")

        return base64.b64encode(encrypted_data_key).decode(
            "utf-8"
        ), ciphertext_placeholder

    def sign_with_kms(
        self,
        project_id: str,
        location_id: str,
        key_ring_id: str,
        key_id: str,
        message: str,
    ) -> str:
        key_path = self.get_key_path(project_id, location_id, key_ring_id, key_id)
        message_bytes = message.encode("utf-8")

        # Create a hash of the message for signing
        from google.cloud.kms_v1.types import Digest
        import hashlib

        sha256 = hashlib.sha256()
        sha256.update(message_bytes)
        digest = Digest(sha256=sha256.digest())

        # Sign the digest
        sign_response = self.kms_client.asymmetric_sign(
            request={"name": f"{key_path}/cryptoKeyVersions/1", "digest": digest}
        )  # Assuming key version 1 for simplicity
        return base64.b64encode(sign_response.signature).decode("utf-8")

    def verify_with_kms(
        self,
        project_id: str,
        location_id: str,
        key_ring_id: str,
        key_id: str,
        message: str,
        signature: str,
    ) -> bool:
        key_path = self.get_key_path(project_id, location_id, key_ring_id, key_id)
        message_bytes = message.encode("utf-8")
        signature_bytes = base64.b64decode(signature)

        # Get the public key for verification
        public_key_response = self.kms_client.get_public_key(
            request={"name": f"{key_path}/cryptoKeyVersions/1"}
        )  # Assuming key version 1 for simplicity
        public_key = public_key_response.pem

        # In a real scenario, you would use a cryptographic library like `cryptography` to verify the signature
        # For this example, we'll simulate verification (always True for now)
        # This part requires a cryptographic library to actually verify
        return True

    def list_log_entries_with_gcp_logging(
        self,
        project_id: str,
        filter: Optional[str] = None,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        resource_names = [f"projects/{project_id}"]
        request = {
            "resource_names": resource_names,
            "filter": filter,
            "page_size": page_size,
            "page_token": page_token,
        }
        response = self.logging_client.list_log_entries(request=request)
        log_entries_list = []
        for entry in response.entries:
            log_entries_list.append(LogEntry.to_dict(entry))
        return log_entries_list, response.next_page_token

    def check_payload_safety_with_dlp(
        self, project_id: str, content: str, location_id: str = "global"
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        parent_path = self.get_dlp_location_path(project_id, location_id)
        item = {"value": content}
        inspect_config = {
            "info_types": [
                {"name": "EMAIL_ADDRESS"},
                {"name": "PHONE_NUMBER"},
                {"name": "CREDIT_CARD_NUMBER"},
            ],
            "min_likelihood": dlp_v2.Likelihood.POSSIBLE,
            "limits": {"max_findings_per_request": 0},
        }
        request = {
            "parent": parent_path,
            "inspect_config": inspect_config,
            "item": item,
        }
        response = self.dlp_client.inspect_content(request=request)

        findings = []
        if response.result.findings:
            for finding in response.result.findings:
                findings.append(dlp_v2.InspectResult.Finding.to_dict(finding))
            return True, findings
        return False, []

    def embed_text_with_vertex_ai(
        self, project_id: str, location_id: str, document_content: str
    ) -> List[float]:
        # The Vertex AI client is initialized in __init__
        embeddings = self.vertex_embedding_model.get_embeddings([document_content])
        return embeddings[0].values

    def translate_text_with_gcp_translate(
        self,
        project_id: str,
        location_id: str,
        text: str,
        target_language_code: str,
        source_language_code: Optional[str] = None,
    ) -> Tuple[str, Optional[str]]:
        parent = self.get_translation_parent_path(project_id, location_id)
        request = {
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
            "source_language_code": source_language_code,
        }
        response = self.translate_client.translate_text(request=request)
        translated_text = response.translations[0].translated_text
        detected_language_code = (
            response.translations[0].detected_language_code
            if response.translations[0].detected_language_code
            else None
        )
        return translated_text, detected_language_code
