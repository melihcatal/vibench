# LOCAL HELPER - Defines request, response, and normalization utilities for Batch Speech-to-Text

from typing import Dict, Any

# Typedef for standardized transcription result
TranscriptionResult = Dict[str, Any]

# Mapping of provider-specific field names to our canonical model
PROVIDER_FIELD_MAP = {
    "IBM Watson Speech to Text": {
        "job_id": "result_id",
        "status": "status",
        "transcript": "results.0.alternatives.0.transcript",
        "timestamps": "results.0.alternatives.0.timestamps",
        "speaker_labels": "results.0.alternatives.0.speaker_labels",
    }
}


def normalize_response(provider: str, raw: Dict[str, Any]) -> TranscriptionResult:
    """Converts a provider-specific raw response into a normalized dictionary with canonical keys.

    Args:
        provider (str): Name of the provider (e.g., 'IBM Watson Speech to Text').
        raw (dict): The raw response JSON from the provider's SDK/API.

    Returns:
        dict: Normalized result containing job_id, status, transcript, timestamps, and speaker_labels.
    """
    mapping = PROVIDER_FIELD_MAP.get(provider)
    if not mapping:
        raise ValueError(f"Unsupported provider: {provider}")
    normalized = {
        "job_id": raw.get(mapping["job_id"]),
        "status": raw.get(mapping["status"]),
        "transcript": raw.get(mapping["transcript"]),
        "timestamps": raw.get(mapping["timestamps"]),
        "speaker_labels": raw.get(mapping["speaker_labels"]) or [],
    }
    return normalized
