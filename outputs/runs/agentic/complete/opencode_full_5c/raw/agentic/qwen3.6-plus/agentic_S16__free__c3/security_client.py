import os
from typing import Optional
import requests

from security_models import (
    VaultConfig,
    SecretRequest,
    SecretResponse,
    normalize_vault_response,
)


class VaultSecretsClient:
    def __init__(self, config: Optional[VaultConfig] = None):
        self.config = config or VaultConfig.from_env()
        self._session = requests.Session()
        self._session.headers.update(
            {
                "X-Vault-Token": self.config.token,
                "Content-Type": "application/json",
            }
        )
        if self.config.namespace:
            self._session.headers["X-Vault-Namespace"] = self.config.namespace
        self._session.verify = self.config.verify_tls

    @property
    def base_url(self) -> str:
        return self.config.address.rstrip("/")

    def _build_secret_url(self, path: str, mount_point: Optional[str] = None) -> str:
        mount = mount_point or self.config.kv_mount
        if self.config.api_version == "v2":
            return f"{self.base_url}/v1/{mount}/data/{path}"
        return f"{self.base_url}/v1/{mount}/{path}"

    def _build_metadata_url(self, path: str, mount_point: Optional[str] = None) -> str:
        mount = mount_point or self.config.kv_mount
        return f"{self.base_url}/v1/{mount}/metadata/{path}"

    def read_secret(self, request: SecretRequest) -> SecretResponse:
        url = self._build_secret_url(request.secret_path, request.mount_point)
        params = {}
        if request.version is not None:
            params["version"] = request.version

        response = self._session.get(url, params=params, timeout=self.config.timeout)
        response.raise_for_status()

        raw = response.json()
        return normalize_vault_response(raw, request.secret_path, request.field)

    def read_secret_metadata(
        self, path: str, mount_point: Optional[str] = None
    ) -> dict:
        url = self._build_metadata_url(path, mount_point)
        response = self._session.get(url, timeout=self.config.timeout)
        response.raise_for_status()
        return response.json()

    def read_secret_version(
        self, path: str, version: int, mount_point: Optional[str] = None
    ) -> SecretResponse:
        request = SecretRequest(
            secret_path=path,
            version=version,
            mount_point=mount_point,
        )
        return self.read_secret(request)

    def get_rotation_info(self, path: str, mount_point: Optional[str] = None) -> dict:
        metadata = self.read_secret_metadata(path, mount_point)
        data = metadata.get("data", metadata)
        versions = data.get("versions", {})
        return {
            "current_version": data.get("current_version"),
            "max_versions": data.get("max_versions"),
            "versions": versions,
            "deletion_time": data.get("deletion_time"),
            "destroyed": data.get("destroyed"),
        }

    def close(self):
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def get_vault_client() -> VaultSecretsClient:
    return VaultSecretsClient()
