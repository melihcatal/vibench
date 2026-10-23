from typing import TypedDict

class InvocationRequest(TypedDict):
    model: str
    deployment: str
    prompt: str

class InvocationResponse(TypedDict):
    model_output: str
    usage: dict
    provider_metadata: dict

# Utility for normalizing provider metadata (e.g., flattening dicts)

def normalize_metadata(raw_metadata: dict) -> dict:
    # Placeholder: perform required flattening or renaming
    return raw_metadata