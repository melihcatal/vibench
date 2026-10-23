# speech_models.py
import os
from typing import Dict, Any, List

# Utilities for request/response normalization and basic model management


class SpeechModels:
    """Local abstraction for mapping provider model identifiers to internal names."""

    # Mapping example for AssemblyAI models
    MODEL_MAP = {
        "assemblyai": {
            "model_id": "assemblyai/english",
            "description": "English transcription model",
        }
    }

    @staticmethod
    def get_model_info(provider: str) -> Dict[str, Any]:
        """Returns model information for a provider."""
        return SpeechModels.MODEL_MAP.get(provider.lower(), {})

    @staticmethod
    def normalize_response(raw: Any) -> Any:
        """Naïve normalization helper that can be extended per provider."""
        # Simple type preservation; replace with provider-specific logic as needed
        if isinstance(raw, dict):
            return {k: SpeechModels.normalize_response(v) for k, v in raw.items()}
        elif isinstance(raw, list):
            return [SpeechModels.normalize_response(item) for item in raw]
        return raw

    @staticmethod
    def detect_provider(response: Any) -> str:
        """Detects which provider generated the response (dummy implementation)."""
        # Return a placeholder based on response shape
        if isinstance(response, dict) and "job_id" in response:
            return "assemblyai"
        return "unknown"


# Example usage (not executed in this file)
# model_info = SpeechModels.get_model_info("assemblyai")
# print(model_info)
