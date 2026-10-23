import os
import json
from typing import Dict, Any, Optional
from huggingface_hub import InferenceApi


class ManagedModelClient:
    """
    Local helper that abstracts provider selection, authentication, and request
    preparation.  Currently supports Hugging Face Inference API natively.
    """
    def __init__(self,
                 provider: str = "huggingface",
                 token: Optional[str] = None,
                 model_id: Optional[str] = None) -> None:
        self.provider = provider
        # Store credentials for later SDKs (e.g., huggingface_hub client)
        self.token = token
        self.model_id = model_id
        # For Hugging Face we use the inference API client directly
        self.inference_api: Optional[InferenceApi] = None
        self._initialize()

    def _initialize(self) -> None:
        if self.provider == "huggingface":
            if not self.token:
                raise RuntimeError("For Hugging Face, set HF_TOKEN environment variable")
            # The InferenceApi constructor reads HF_TOKEN from os.environ automatically.
            # Explicitly set it to protect callers who may not rely on env vars.
            os.environ["HF_TOKEN"] = self.token
            # No further init needed; inference calls are lazy per request
            self.inference_api = InferenceApi(repo_id=self.model_id)
        else:
            raise ValueError(f"Provider {self.provider} not implemented in this helper")

    def invoke(self, request: Any, stream: bool = False) -> Any:
        """
        Invoke the underlying provider client.  For Hugging Face, we call
        inference_api.generate() with or without streaming.
        """
        if self.provider != "huggingface":
            raise NotImplementedError("Only Hugging Face provider is supported in this mock client")
        # Prepare payload from request (duck‑typed)
        payload = {
            "inputs": request.inputs,
            "parameters": request.parameters
        }
        # Hugging Face client supports streaming via its low‑level _generate_stream method.
        if stream:
            # Return an iterator yielding raw JSON chunks
            return self.inference_api._generate_stream(payload, stream=True)
        else:
            # Standard single response
            return self.inference_api.generate(payload)

    def request_id(self) -> Optional[str]:
        """Return the request identifier if available from the provider response."""
        return getattr(self, "_request_id", None)

    @property
    def raw(self) -> Dict[str, Any]:
        """Return any raw payload captured from the provider response."""
        return getattr(self, "_raw", {})