from __future__ import annotations

from security_client import AzureKeyVaultSecurityClient, load_security_config


if __name__ == "__main__":
    client = AzureKeyVaultSecurityClient(load_security_config())
    client.translate_note("Encryption controls reviewed", target_language="fr")
