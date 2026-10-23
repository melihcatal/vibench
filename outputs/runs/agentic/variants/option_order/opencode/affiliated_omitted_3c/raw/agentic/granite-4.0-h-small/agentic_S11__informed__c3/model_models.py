from typing import List, Dict, Any, Optional


class ModelInvocationRequest:
    """
    Encapsulates the payload required to invoke a managed generative model.
    ","""

    def __init__(
        self,
        messages: List[Dict[str, Any]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ):
        """
        Args:
            messages: List of (role, content) pairs matching the provider's chat format.
            temperature: Sampling temperature.
            max_tokens: Maximum output token limit.
            **kwargs: Additional provider‑specific parameters (e.g., top_p, n)."""
        self.messages = messages
        self.temperature = temperature
        self.max_tokens = max_tokens
        # Store any extra fields for later normalization
        self.extra = kwargs


class ModelInvocationResponse:
    """
    Normalized response from a model invocation.
    ","""

    def __init__(
        self,
        output: str,
        usage: Optional[Dict[str, Any]] = None,
        resource_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.output = output  # Human‑readable text result
        self.usage = (
            usage  # Provider usage info (prompt_tokens, completion_tokens, etc.)
        )
        self.resource_id = resource_id  # Request‑level identifier (often a log ID)
        self.metadata = (
            metadata  # Extra metadata (latency, token counts, model version, etc.)
        )


class ResourceQuery:
    """
    Describes a request to resolve a provider resource (model, deployment, etc.) before invocation.
    ","""

    def __init__(
        self,
        resource_type: str,
        provider: str,
        filters: Optional[Dict[str, Any]] = None,
    ):
        """
        Args:
            resource_type: e.g., "deployment", "model", "endpoint".
            provider: Alias used by the resolver (e.g., "azure_openai").
            filters: Provider‑specific filter criteria (name, version, etc.)."""
        self.resource_type = resource_type
        self.provider = provider
        self.filters = filters or {}


class ResourceSelector:
    """
    Holds resolved identifiers for a requested provider resource.
    ","""

    def __init__(
        self,
        provider: str,
        deployment_id: Optional[str] = None,
        model_id: Optional[str] = None,
    ):
        self.provider = provider
        self.deployment_id = deployment_id
        self.model_id = model_id


class StreamedOutputChunk:
    """
    Representation of a single chunk emitted during streaming generation.
    The raw structure mirrors the provider SDK's chunk format.
    ","""

    def __init__(self, chunk: Dict[str, Any]):
        self.chunk = chunk

    def __repr__(self) -> str:
        return json.dumps(self.chunk, indent=2)
