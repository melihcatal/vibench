"""[HELPER] model_models.py - Define local request, response, and normalization helpers for Managed Model Platform Workflow"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PlatformInvocationResult:
    """
    Generic container for a model invocation result.

    Attributes:
        data: Raw output returned by the provider (could be dict, list, or custom object).
        provider: Human‑readable identifier ("Amazon Bedrock", "Vertex AI", ...).
    """

    data: Any
    provider: str

    def to_dict(self) -> Dict[str, Any]:
        """Normalize to a plain dictionary when possible."""
        if isinstance(self.data, Dict):
            return self.data
        return {"raw": self.data}


@dataclass
class StreamedGeneration:
    """
    Holds streamed text and the final raw provider response.

    Attributes:
        text: Concatenated full response.
        raw_response: The last/residual provider response object (may be None).
    """

    text: str
    raw_response: Optional[Any]


@dataclass
class PlatformMetadataResult:
    """
    Bundles primary output with additional metadata from the provider.

    Attributes:
        data: Primary model output (usually a dict or string).
        metadata: Dictionary containing extra provider fields.
    """

    data: Any
    metadata: Dict[str, Any]
