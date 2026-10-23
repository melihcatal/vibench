# rotation_summary.py
import json
from typing import List, Dict
from security_client import rotate_secret_version
from security_models import FetchSecretRequest, FetchSecretResponse


def summarize_secret_rotations(queries: List[FetchSecretRequest]) -> List[Dict]:
    """Generate a summary of secret rotation status for each requested secret.
    Calls rotate_secret_version for each secret and extracts status fields.
    Returns a list of human‑readable summary dictionaries.
    """
    summaries = []
    for req in queries:
        # Example: treat version 'staged' as the pending rotation value
        result = rotate_secret_version(req["secret_name"], version="staged")
        # Extract relevant fields
        meta = result["metadata"]
        value = result["resources"][0]["secret_data"].get("text", "no value")
        summaries.append(
            {
                "secret_name": meta.get("name"),
                "staged_version": meta.get("version_id"),
                "status": "rotated" if meta.get("status") == "active" else "pending",
                "value": value,
            }
        )
    return summaries


# Example execution (will raise if API keys not configured)
if __name__ == "__main__":
    sample_queries = [
        {"secret_name": "api-key-secret", "secret_type": "arbitrary"},
        {"secret_name": "db-conn-secret", "secret_type": "arbitrary"},
    ]
    summary = summarize_secret_rotations(sample_queries)
    print(json.dumps(summary, indent=2))
