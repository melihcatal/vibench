from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from typing import Optional

from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
from azure.keyvault.secrets import SecretClient
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm, SignatureAlgorithm


@dataclass(frozen=True)
class SecurityConfig:
    vault_url: str
    key_name: str
    key_version: Optional[str] = None
    secret_name: Optional[str] = None


def load_config(prefix: str = "AZURE_KEYVAULT") -> SecurityConfig:
    vault_url = os.environ[f"{prefix}_URL"]
    key_name = os.environ[f"{prefix}_KEY_NAME"]
    key_version = os.getenv(f"{prefix}_KEY_VERSION")
    secret_name = os.getenv(f"{prefix}_SECRET_NAME")
    return SecurityConfig(vault_url=vault_url, key_name=key_name, key_version=key_version, secret_name=secret_name)


def credential():
    return DefaultAzureCredential(exclude_interactive_browser_credential=False)


def key_client(config: SecurityConfig) -> KeyClient:
    return KeyClient(vault_url=config.vault_url, credential=credential())


def secret_client(config: SecurityConfig) -> SecretClient:
    return SecretClient(vault_url=config.vault_url, credential=credential())


def cryptography_client(config: SecurityConfig) -> CryptographyClient:
    key = key_client(config).get_key(config.key_name, config.key_version)
    return CryptographyClient(key, credential=credential())


def b64encode(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def b64decode(data: str) -> bytes:
    return base64.b64decode(data.encode("utf-8"))


def encrypt_with_key(config: SecurityConfig, plaintext: bytes, algorithm: EncryptionAlgorithm = EncryptionAlgorithm.rsa_oaep) -> dict:
    client = cryptography_client(config)
    result = client.encrypt(algorithm=algorithm, plaintext=plaintext)
    return {"key_id": result.key_id, "algorithm": result.algorithm.name, "ciphertext": b64encode(result.ciphertext)}


def decrypt_with_key(config: SecurityConfig, ciphertext: bytes, algorithm: EncryptionAlgorithm = EncryptionAlgorithm.rsa_oaep) -> dict:
    client = cryptography_client(config)
    result = client.decrypt(algorithm=algorithm, ciphertext=ciphertext)
    return {"key_id": result.key_id, "plaintext": result.plaintext}


def sign_with_key(config: SecurityConfig, digest: bytes, algorithm: SignatureAlgorithm = SignatureAlgorithm.rs256) -> dict:
    client = cryptography_client(config)
    result = client.sign(algorithm=algorithm, digest=digest)
    return {"key_id": result.key_id, "signature": b64encode(result.signature), "algorithm": result.algorithm.name}


def verify_with_key(config: SecurityConfig, digest: bytes, signature: bytes, algorithm: SignatureAlgorithm = SignatureAlgorithm.rs256) -> dict:
    client = cryptography_client(config)
    result = client.verify(algorithm=algorithm, digest=digest, signature=signature)
    return {"key_id": result.key_id, "is_valid": result.is_valid, "algorithm": result.algorithm.name}
