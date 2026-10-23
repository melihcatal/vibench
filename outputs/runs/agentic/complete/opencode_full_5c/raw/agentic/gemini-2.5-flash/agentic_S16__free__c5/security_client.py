import os
from google.cloud import secretmanager_v1 as secretmanager
from security_models import SecretPayload, SecretMetadata
from typing import Dict, Optional


class SecretManagerHelper:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.client = secretmanager.SecretManagerServiceClient()

    def _get_secret_name(self, secret_id: str, version_id: str = "latest") -> str:
        return self.client.secret_version_path(self.project_id, secret_id, version_id)

    def get_secret_value(
        self, secret_id: str, version_id: str = "latest"
    ) -> SecretPayload:
        name = self._get_secret_name(secret_id, version_id)
        response = self.client.access_secret_version(request={"name": name})
        return SecretPayload(
            name=response.name, data=response.payload.data, version=version_id
        )

    def get_secret_metadata(self, secret_id: str) -> SecretMetadata:
        name = self.client.secret_path(self.project_id, secret_id)
        response = self.client.get_secret(request={"name": name})
        return SecretMetadata(
            name=response.name,
            project_id=self.project_id,
            secret_id=secret_id,
            labels=dict(response.labels),
            annotations=dict(response.annotations),
            create_time=str(response.create_time),
            destroy_time=str(
                response.replication.automatic.customer_managed_encryption.kms_key_name
            )
            if response.replication.automatic.customer_managed_encryption
            else None,
            state=str(response.state).split(".")[-1],
        )

    def list_secret_versions(self, secret_id: str) -> list[Dict]:
        parent = self.client.secret_path(self.project_id, secret_id)
        versions = []
        for version in self.client.list_secret_versions(request={"parent": parent}):
            versions.append(
                {
                    "name": version.name,
                    "state": str(version.state).split(".")[-1],
                    "create_time": str(version.create_time),
                    "destroy_time": str(version.destroy_time)
                    if version.destroy_time
                    else None,
                    "etag": version.etag,
                    "scheduled_destroy_time": str(version.scheduled_destroy_time)
                    if version.scheduled_destroy_time
                    else None,
                }
            )
        return versions

    def add_secret_version(self, secret_id: str, payload: bytes) -> str:
        parent = self.client.secret_path(self.project_id, secret_id)
        response = self.client.add_secret_version(
            request={"parent": parent, "payload": {"data": payload}}
        )
        return response.name
