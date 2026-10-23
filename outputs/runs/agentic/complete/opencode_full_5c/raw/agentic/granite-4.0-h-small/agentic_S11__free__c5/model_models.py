# model_models.py
# [HELPER]
# Define local request, response, and normalization helpers for Managed Model Platform Workflow

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------
@dataclass
class ModelInvocationRequest:
    project_id: str
    deployment_id: str
    input_text: str
    profile: str = "default"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ModelResourceRequest:
    project_id: str
    name: str
    type: str = "model"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class StreamingRequest:
    project_id: str
    deployment_id: str
    prompt: str
    profile: str = "default"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class MetadataRequest:
    project_id: str
    deployment_id: str
    run_id: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

# ---------------------------------------------------------------------------
# Response models (normalized across providers)
# ---------------------------------------------------------------------------
@dataclass
class ModelInvocationResponse:
    run_id: str
    output_text: str
    usage: UsageInfo
    metadata: Optional[Dict[str, Any]] = None

    @staticmethod
def from_raw(raw: Dict[str, Any]) -> ModelInvocationResponse:
        return ModelInvocationResponse(
            run_id=raw["run_id"],
            output_text=raw["output_text"],
            usage=UsageInfo.from_dict(raw["usage"]),
            metadata=raw.get("metadata"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ModelResourceResponse:
    resource_id: str
    status: str

    @staticmethod
def from_raw(raw: Dict[str, Any]) -> ModelResourceResponse:
        return ModelResourceResponse(**raw)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class StreamingResponse:
    # Wraps the raw streaming generator from the provider SDK
    raw_stream: Any

    def __iter__(self):
        return self.raw_stream

    def to_dict(self) -> Dict[str, Any]:
        return {"stream_id": self.raw_stream.stream_id}

@dataclass
class MetadataResponse:
    run_id: str
    usage: UsageInfo
    metadata: Dict[str, Any]

    @staticmethod
def from_raw(raw: Dict[str, Any]) -> MetadataResponse:
        return MetadataResponse(
            run_id=raw["run_id"],
            usage=UsageInfo.from_dict(raw["usage"]),
            metadata=raw["metadata"],
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class StreamingChunk:
    chunk_text: str
    provider_chunk: Any  # preserve original provider object

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.chunk_text, "provider_chunk": asdict(self.provider_chunk)}

@dataclass
class UsageInfo:
    total_tokens: int
    prompt_tokens: int
    completion_tokens: int
    model: str

    @staticmethod
def from_dict(data: Dict[str, Any]) -> UsageInfo:
        return UsageInfo(
            total_tokens=data["total_tokens"],
            prompt_tokens=data["prompt_tokens"],
            completion_tokens=data["completion_tokens"],
            model=data["model"],
        )

# ---------------------------------------------------------------------------
# Example conversion utilities (to be used by SAME-SCENARIO files)
# ---------------------------------------------------------------------------

def normalize_invocation(raw: Dict[str, Any]) -> ModelInvocationResponse:
    return ModelInvocationResponse.from_raw(raw)


def normalize_resource(raw: Dict[str, Any]) -> ModelResourceResponse:
    return ModelResourceResponse.from_raw(raw)


def normalize_metadata(raw: Dict[str, Any]) -> MetadataResponse:
    return MetadataResponse.from_raw(raw)

# ---------------------------------------------------------------------------
# Example usage (uncomment to test locally)
# ---------------------------------------------------------------------------
# if __name__ == "__main__":
#     print(ModelInvocationRequest(project_id="p1", deployment_id="d1", input_text="Hi"))