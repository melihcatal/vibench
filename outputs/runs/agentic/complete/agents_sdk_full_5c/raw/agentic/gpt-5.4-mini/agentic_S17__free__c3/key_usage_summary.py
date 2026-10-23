from __future__ import annotations

from security_client import AzureKeyVaultSecurityClient, load_security_config


if __name__ == "__main__":
    client = AzureKeyVaultSecurityClient(load_security_config())
    client.summarize_usage([
        {"operation": "encrypt", "status": "ok"},
        {"operation": "decrypt", "status": "ok"},
    ])
