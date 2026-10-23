from sentence_transformers import SentenceTransformer
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import numpy as np
import os


class SecretAuditEmbedder:
    """
    Embeds secret audit notes for semantic search using Sentence Transformers.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_secret_audit_notes(
        self, key_vault_name: str, secret_name: str
    ) -> np.ndarray:
        """
        Embeds audit notes for a secret from Azure Key Vault.

        Args:
            key_vault_name: Name of the Azure Key Vault.
            secret_name: Name of the secret to fetch audit notes for.

        Returns:
            Embedding vector as a numpy array.
        """
        key_vault_uri = f"https://{key_vault_name}.vault.azure.net"
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=key_vault_uri, credential=credential)

        # Fetch secret properties to get audit notes
        secret_properties = client.get_secret_properties(secret_name)
        audit_notes = (
            secret_properties.tags.get("audit_notes", "")
            if secret_properties.tags
            else ""
        )

        if not audit_notes:
            raise ValueError("No audit notes found for the secret.")

        embedding = self.model.encode(audit_notes)
        return embedding
