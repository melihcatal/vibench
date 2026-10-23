# [HELPER] model_client.py
# Local configuration and client helper utilities for Managed Model Platform Workflow

import os
from dataclasses import dataclass
from typing import Any, Dict

# -----------------------------------------------------------------------------
# Configuration Loading
# -----------------------------------------------------------------------------


def load_env_config() -> Dict[str, str]:
    """Load platform-specific environment variables for IBM watsonx.ai."""
    return {
        "API_KEY": os.getenv("WATSONX_API_KEY"),
        "PROJECT_ID": os.getenv("WATSONX_PROJECT_ID"),
    }


# -----------------------------------------------------------------------------
# Client Factory
# -----------------------------------------------------------------------------


@dataclass
class ManagedModelClient:
    """Thin wrapper around the watsonx.ai SDK client."""

    api_key: str
    project_id: str
    max_tokens: int = 256

    @property
    def client(self):
        """Instantiate the watsonx.ai APIClient only when needed."""
        from ibm_watsonx_ai import APIClient

        return APIClient(api_key=self.api_key, project_id=self.project_id)

    def invoke(self, deployment_id: str, prompt: str) -> Dict[str, Any]:
        """Invoke a deployment and return response + metadata."""
        client = self.client()
        resp = client.text_generation.complete(
            deployment_name=f"{deployment_id}---text-completion",
            messages=[{"content": prompt}],
            max_tokens=self.max_tokens,
        )
        # Basic normalisation (you can extend as needed)
        result = {
            "output": resp.get_result(),
            "request_id": resp.get_request_id(),
            "usage": resp.get_usage(),
        }
        return result


# -----------------------------------------------------------------------------
# Helper Function (singleton style usage)
# -----------------------------------------------------------------------------

_config: Any = None


def get_client() -> ManagedModelClient:
    """Return a pre-configured client using env vars; lazy loads on first call."""
    global _config
    if _config is None:
        cfg = load_env_config()
        if not cfg["API_KEY"] or not cfg["PROJECT_ID"]:
            raise RuntimeError(
                "Environment variables WATSONX_API_KEY and WATSONX_PROJECT_ID must be set"
            )
        _config = ManagedModelClient(
            api_key=cfg["API_KEY"], project_id=cfg["PROJECT_ID"]
        )
    return _config


# Example usage (uncomment to test locally)
# client = get_client()
# response = client.invoke('my-deployment-id', 'Hello, world!')
# print(response)
