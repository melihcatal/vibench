import os
import json
import httpx


class ManagedModelClient:
    def __init__(self, project_id, deployment_id, api_key=None):
        self.project_id = project_id
        self.deployment_id = deployment_id
        self.api_key = api_key or os.getenv("MODEL_API_KEY")
        self.base_url = "https://api.openai.com/v1"

    async def invoke(self, payload):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/projects/{self.project_id}/deployments/{self.deployment_id}/generate",
                json=payload,
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            resp.raise_for_status()
            return resp.json()

    async def stream(self, prompt):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/projects/{self.project_id}/deployments/{self.deployment_id}/generate_streaming",
                json={"prompt": prompt},
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            resp.raise_for_status()
            # Yield chunks as they arrive (placeholder)
            for chunk in resp.json().get("chunks", []):
                yield json.dumps(chunk)
