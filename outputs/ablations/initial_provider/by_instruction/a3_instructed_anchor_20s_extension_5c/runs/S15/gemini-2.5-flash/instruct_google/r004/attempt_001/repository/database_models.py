import json

def normalize_document_data(data: dict) -> dict:
    """Normalizes document data before upserting."
    # Example: Ensure all keys are strings, handle serialization if necessary
    # For Firestore, basic dicts are usually fine, but this is a placeholder for complex types.
    return json.loads(json.dumps(data)) # Simple way to ensure JSON compatibility
