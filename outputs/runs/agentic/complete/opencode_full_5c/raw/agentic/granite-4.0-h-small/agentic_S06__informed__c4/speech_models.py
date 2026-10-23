# speech_models.py
import os
from typing import Dict, Any, Optional

# ----------------------
# Provider‑agnostic request/response models
# ----------------------


class SynthesisRequest:
    """Container for parameters passed to a TTS engine."""

    def __init__(
        self, text: str, voice: Optional[str] = None, format: str = "wav", **extra
    ):
        self.text = text
        self.voice = voice
        self.format = format
        self.extra = extra  # free‑form extra fields per provider


class SynthesisResponse:
    """Container for the raw output of a TTS synthesis call."""

    def __init__(self, audio_bytes: bytes, metadata: Optional[Dict[str, Any]] = None):
        self.audio_bytes = audio_bytes
        self.metadata = metadata or {}


class SafetyCheckResult:
    """Result of a content‑safety evaluation."""

    def __init__(self, clean: bool, flagged_items: Optional[list] = None):
        self.clean = clean
        self.flagged_items = flagged_items or []


class EmbeddingRequest:
    """Request for generating embeddings for a script or voice asset."""

    def __init__(self, text: str, model_id: str, **extra):
        self.text = text
        self.model_id = model_id
        self.extra = extra


class EmbeddingResponse:
    """Container for embedding vectors and optional metadata."""

    def __init__(self, vector: list[float], metadata: Optional[Dict[str, Any]] = None):
        self.vector = vector
        self.metadata = metadata or {}


# ----------------------
# Helper utilities
# ----------------------


def build_embedding_payload(request: EmbeddingRequest) -> Dict[str, Any]:
    """Create a provider‑agnostic payload for embedding APIs."""
    payload = {"text": request.text, "model": request.model_id}
    payload.update(request.extra)
    return payload


def build_safety_payload(text: str, provider: str) -> Dict[str, Any]:
    """Construct safety‑check request payload for a given provider."""
    if provider == "tisane":
        return {"text": text, "categories": ["TOXICITY", "HATE"]}
    elif provider == "perspective":
        return {"comment": text}
    elif provider == "watsonx":
        return {"content": text, "severity": "MODERATE"}
    elif provider == "aws":
        return {"text": text, "content_type": "plain"}
    elif provider == "alibaba":
        return {"content": text, "category": "TOXICITY"}
    return {"text": text}


# ----------------------
# Example usage (stand‑alone)
# ----------------------
if __name__ == "__main__":
    req = SynthesisRequest(text="Test script", voice="default", format="opus")
    print("Request:", req.text, req.voice, req.format)
    resp = SynthesisResponse(audio_bytes=b"fake audio")
    print("Response bytes length:", len(resp.audio_bytes))
    safety = SafetyCheckResult(clean=True, flagged_items=["punchline"])
    print("Safety clean?", safety.clean)
    embed = EmbeddingRequest("A quick brown fox", model_id="text-embedding-ada-002")
    embed_payload = build_embedding_payload(embed)
    print("Embed payload:", embed_payload)
