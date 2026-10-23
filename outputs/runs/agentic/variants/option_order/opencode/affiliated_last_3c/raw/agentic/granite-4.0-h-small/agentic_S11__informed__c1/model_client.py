import os
import json
from typing import Any, Dict


class ManagedModelClient:
    """Lightweight wrapper around a concrete managed‑model provider.

    The class encapsulates authentication, client instantiation, and a generic
    `invoke` method that returns a dict with keys `output`, `metadata`, and `raw`.
    """

    # ----------------------------------------------------------------------
    # Provider identification – the concrete provider used in this implementation
    # ----------------------------------------------------------------------
    PROVIDER = "Azure OpenAI Service"
    # Provider‑specific configuration loaded from environment variables
    ENDPOINT = os.getenv(
        "AZURE_OPENAI_ENDPOINT"
    )  # e.g. https://<resource>.openai.azure.com/
    API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    # ----------------------------------------------------------------------

    def __init__(self):
        # Minimal runtime validation – the service raises an exception if the
        # required env vars are missing, which the caller must handle.
        if not (self.ENDPOINT and self.API_KEY):
            raise RuntimeError(
                f"{self.PROVIDER} requires AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY env vars"
            )
        # Concrete client import – this makes the provider explicit in the file
        from openai import AzureOpenAI  # type: ignore

        # Store the low‑level client for reuse
        self._client = AzureOpenAI(
            azure_endpoint=self.ENDPOINT,
            api_key=self.API_KEY,
            api_type="azure",
            api_version="2023-05-15",
        )

    def invoke(
        self,
        project: str,
        deployment: str,
        messages: list,
        model: str | None = None,
    ) -> Dict[str, Any]:
        """Call the provider and return a normalized dict.

        Args:
            project: Azure resource group / project name.
            deployment: Deployment / inference profile name.
            messages: List of dicts in OpenAI‑compatible format, e.g.
                      [{"role": "user", "content": "Hello"}].
            model: Optional explicit model identifier (overrides deployment mapping).

        Returns:
            dict: Normalized response with keys `output`, `metadata`, `raw`.
        """
        # Build the request payload; Azure OpenAI expects a slightly different shape
        payload = {
            "project": project,
            "deployment": deployment,
            "messages": messages,
            "model": model or deployment,
        }
        raw_response = self._client.chat.completions.create(**payload)
        # Azure OpenAI returns a Response object; extract needed fields
        output = raw_response.choices[0].message.content if raw_response.choices else ""
        metadata = {
            "usage": {
                "prompt_tokens": raw_response.usage.prompt_tokens,
                "completion_tokens": raw_response.usage.completion_tokens,
                "total_tokens": raw_response.usage.total_tokens,
            },
            "deployment_id": deployment,
            "model_id": model or deployment,
        }
        return {
            "output": output,
            "metadata": metadata,
            "raw": raw_response,
        }
