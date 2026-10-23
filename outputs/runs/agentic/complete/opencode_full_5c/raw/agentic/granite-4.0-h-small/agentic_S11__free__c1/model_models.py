from typing import Any, Dict, List


# Normalized request object shared across workflow steps
class ModelInvocationRequest:
    def __init__(self, project_id: str, deployment_id: str, payload: Dict[str, Any]):
        self.project_id = project_id
        self.deployment_id = deployment_id
        self.payload = payload


class ModelInvocationResponse:
    def __init__(self, output: Any, metadata: Dict[str, Any]):
        self.output = output  # Normalized model output (text, JSON, etc.)
        self.metadata = metadata  # Provider‑specific metadata (usage, request_id, model_handle, ...)


class ModelStreamingResponse:
    def __init__(self, chunks: List[str], metadata: Dict[str, Any]):
        self.chunks = chunks  # List of raw chunks received during streaming
        self.metadata = metadata  # Same metadata as ModelInvocationResponse


class PlatformMetadata:
    def __init__(self, usage: Dict[str, int], request_id: str, model_handle: str):
        self.usage = usage  # Tokens or other usage metrics
        self.request_id = request_id
        self.model_handle = model_handle
