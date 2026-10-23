import json


def summarize_rotation(
    old_version: str, new_version: str, status: str = "completed"
) -> dict:
    """Create a concise rotation status summary.

    Args:
        old_version (str): The previous version ID.
        new_version (str): The newly promoted version ID.
        status (str): Overall rotation status (default 'completed').

    Returns:
        dict: JSON-serializable summary payload.
    """
    return {
        "message": "Secret rotation completed",
        "details": {
            "old_version": old_version,
            "new_version": new_version,
            "status": status,
        },
    }


# Example usage (not executed in library)
if __name__ == "__main__":
    print(json.dumps(summarize_rotation("v1", "v2"), indent=2))
