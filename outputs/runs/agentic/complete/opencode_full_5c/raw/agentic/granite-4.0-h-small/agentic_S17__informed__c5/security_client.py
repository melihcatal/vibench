# security_client.py
# Local helper utilities for Key Management and Encryption integration

import os
from typing import Any, Dict

# Provider identifier strings to make the concrete service clear in code

# HashiCorp Vault (via hvac SDK)
VAULT_ADDR = os.getenv("VAULT_ADDR")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")
if not VAULT_ADDR or not VAULT_TOKEN:
    raise RuntimeError("Set VAULT_ADDR and VAULT_TOKEN environment variables")

VAULT_CLIENT = None

# Azure Key Vault Keys (via azure-keyvault-keys SDK)
AZURE_KEY_VAULT_URL = os.getenv("AZURE_KEY_VAULT_URL")
AZURE_KV_CLIENT = None

# Alibaba Cloud KMS (via alibabacloud_kms SDK)
ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
ALIBABA_KMS_CLIENT = None

# Google Cloud KMS (via google-cloud-kms SDK)
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
GoogleKMS_CLIENT = None

# IBM Key Protect (via ibm-key-protect-sdk / requests)
IBM_KEY_PROTECT_APIKEY = os.getenv("IBM_KEY_PROTECT_APIKEY")
IBM_KEY_PROTECT_URL = os.getenv("IBM_KEY_PROTECT_URL")
IBM_KP_CLIENT = None


# General helper to lazily initialize the preferred provider (default: Vault)
def get_kms_client(provider: str = "vault") -> Any:
    global \
        VAULT_CLIENT, \
        AZURE_KV_CLIENT, \
        ALIBABA_KMS_CLIENT, \
        GoogleKMS_CLIENT, \
        IBM_KP_CLIENT
    if provider == "vault":
        if VAULT_CLIENT is None:
            import hvac

            VAULT_CLIENT = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)
        return VAULT_CLIENT
    elif provider == "azure":
        if AZURE_KV_CLIENT is None:
            from azure.keyvault.keys import KeyClient

            AZURE_KV_CLIENT = KeyClient(
                vault_url=AZURE_KEY_VAULT_URL, credential=None
            )  # credential handling delegated to env / Managed Identity
        return AZURE_KV_CLIENT
    elif provider == "alibaba":
        if ALIBABA_KMS_CLIENT is None:
            from alibabacloud_kms.v20220101 import Client

            ALIBABA_KMS_CLIENT = Client(
                access_key_id=ALIBABA_ACCESS_KEY_ID,
                access_key_secret=ALIBABA_ACCESS_KEY_SECRET,
                endpoint=ALIBABA_KMS_ENDPOINT_URL,  # define elsewhere in your config
            )
        return ALIBABA_KMS_CLIENT
    elif provider == "google":
        if GoogleKMS_CLIENT is None:
            from google.cloud import kms_v1

            GoogleKMS_CLIENT = kms_v1.KeyManagementServiceClient()
        return GoogleKMS_CLIENT
    elif provider == "ibm":
        if IBM_KP_CLIENT is None:
            from ibm_key_protect_sdk import KeyProtectServiceV1

            IBM_KP_CLIENT = KeyProtectServiceV1(
                apikey=IBM_KEY_PROTECT_APIKEY,
                service_url=IBM_KEY_PROTECT_URL,
            )
        return IBM_KP_CLIENT
    else:
        raise ValueError(f"Unsupported provider: {provider}")


# Normalization and parsing utilities


def parse_vault_kv_secret(response: Dict[str, Any]) -> Dict[str, Any]:
    """Extract secret data from HashiCorp Vault KV v2 response."""
    # response format: {"data": {"data": {"value": <b64>, "...": ...}, "metadata": {...}}}
    return response["data"]["data"]


# Example helper for generic GET request against any REST endpoint
import requests


def generic_rest_get(url: str, headers: Dict[str, str] = None) -> Any:
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()


# Example helper to wrap a raw key in a human‑readable label


def format_key_label(key_id: str, provider: str) -> str:
    return f"[{provider.upper()}] {key_id}"


# End of module
