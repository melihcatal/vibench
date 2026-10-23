# [SAME-SCENARIO] select_platform_resource.py
# IBM watsonx.ai resource resolution helper

import os
from typing import Dict, Union


class ResourceResolver:
    """
    Helper to resolve a watsonx.ai model, deployment, or inference profile.

    The provider expects a name or ID; this class abstracts the lookup.
    """

    def __init__(self, api_key: str, project_id: str):
        from ibm_watsonx_ai import APIClient

        self.client = APIClient(api_key=api_key, project_id=project_id)

    def resolve_deployment(self, name_or_id: str) -> Dict:
        """Return details of a deployment by name or ID."""
        return self.client.deployments.get_by_name(name_or_id)

    def resolve_model(self, name_or_id: str) -> Dict:
        """Return details of a model by name or ID."""
        return self.client.models.get_by_name(name_or_id)

    def resolve_inference_profile(self, name: str) -> Dict:
        """Return details of an inference profile by name."""
        # watsonx.ai API uses projects/inference_profiles endpoint
        return self.client.inference_profiles.get(name=name)

    @staticmethod
    def from_env() -> "ResourceResolver":
        key = os.getenv("WATSONX_API_KEY")
        proj = os.getenv("WATSONX_PROJECT_ID")
        if not key or not proj:
            raise RuntimeError(
                "Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables"
            )
        return ResourceResolver(key, proj)


# Example usage (not executed during import)
# resolver = ResourceResolver.from_env()
# deployment = resolver.resolve_deployment('my-deployment-id')
# print(deployment)
