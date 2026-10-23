"""Select and resolve a provider-specific model, deployment, or inference resource before invocation.

Resolves an OpenAI managed model identifier using platform capability inspection
and environment-level defaults. Calls OpenAI's models.list endpoint to validate
that the resolved model_id is available for the configured API key.
"""

from __future__ import annotations

import os
from typing import Dict, List, Optional

from openai import OpenAI

from model_client import create_openai_client, resolve_deployment_model, load_openai_config
from model_models import PlatformModelRequest


class ResourceResolver:
    """Resolves an OpenAI platform resource (model) before invocation."""

    def __init__(self, client: Optional[OpenAI] = None) -> None:
        self._client = client or create_openai_client()

    def list_available_models(self) -> List[Dict[str, str]]:
        """Return all OpenAI model resources visible to this API key.

        Uses the OpenAI models.list REST/SDK endpoint.
        """
        models = self._client.models.list()
        return [
            {
                "id": m.id,
                "object": m.object,
                "created": str(m.created),
                "owned_by": m.owned_by,
            }
            for m in models.data
        ]

    def resolve_model(self, model_id: Optional[str] = None) -> str:
        """Resolve a concrete OpenAI model identifier and verify availability.

        Checks the candidate model against the OpenAI models.list endpoint.
        Raises ValueError if the model is not found.
        """
        candidate = resolve_deployment_model(model_id)

        available = self._client.models.list()
        available_ids = {m.id for m in available.data}

        if candidate not in available_ids:
            raise ValueError(
                f"OpenAI model '{candidate}' is not available on this account. "
                f"Available models include: {sorted(available_ids)}"
            )
        return candidate

    def resolve_model_details(self, model_id: Optional[str] = None) -> Dict[str, str]:
        """Return detailed metadata for a resolved OpenAI model resource."""
        resolved_id = self.resolve_model(model_id)
        model_obj = self._client.models.retrieve(resolved_id)
        return {
            "id": model_obj.id,
            "object": model_obj.object,
            "created": str(model_obj.created),
            "owned_by": model_obj.owned_by,
        }

    def build_request(self, messages: List[Dict[str, str]], **kwargs) -> PlatformModelRequest:
        """Build a fully resolved PlatformModelRequest with validated model_id."""
        resolved_model = self.resolve_model(kwargs.pop("model_id", None))
        return PlatformModelRequest(
            model_id=resolved_model,
            messages=messages,
            **kwargs,
        )


def select_platform_resource(
    messages: List[Dict[str, str]],
    model_id: Optional[str] = None,
    client: Optional[OpenAI] = None,
) -> PlatformModelRequest:
    """Top-level helper: resolve resource and return a ready-to-invite request.

    Uses the OpenAI platform SDK to validate the model identifier.
    """
    resolver = ResourceResolver(client=client)
    return resolver.build_request(messages, model_id=model_id)
