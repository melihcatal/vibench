import os

# Managed NoSQL Document Store configuration helpers


def get_database_uri():
    """Select and return the URI/connection string for the chosen managed NoSQL provider.
    Choose one of the concrete services by setting its environment variable.
    """
    # Example environment variables per service (only one should be set in the runtime env)
    providers = {
        "MONGODB_ATLAS_URI": os.getenv("MONGODB_ATLAS_URI"),
        "AZURE_COSMOS_ENDPOINT": os.getenv("AZURE_COSMOS_ENDPOINT"),
        "ALIBABA_CLOUD_ACCESS_KEY_ID": os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        "GOOGLE_APPLICATION_CREDENTIALS": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
    }
    for env, uri in providers.items():
        if uri:
            return uri
    raise RuntimeError(
        "No managed NoSQL credential configured. Set one of the environment variables: %s"
        % list(providers.keys())
    )


def normalize_document(doc):
    """Normalize incoming document payload for the concrete provider.
    This placeholder demonstrates a simple type‑coercion step; replace with provider‑specific handling.
    """
    # Ensure primary_id is present and named appropriately per service
    if not isinstance(doc, dict):
        raise ValueError("Document must be a dict")
    if "primary_id" not in doc:
        raise KeyError("Document missing primary identifier field 'primary_id'")
    # Example: DynamoDB expects string IDs, Firestore prefers snake_case, etc.
    doc["id"] = str(doc.pop("primary_id"))  # unified key
    return doc


def parse_response(response):
    """Parse a raw response from the provider into a common local format.
    Returns a dict with key 'document'.
    """
    # Placeholder – replace with provider‑specific extraction logic
    if not response:
        return {}
    return {"document": response}
