from datetime import datetime
from typing import List


# Helper to summarize rotation status for a list of secrets
def rotation_summary(secrets_status: List[dict]) -> str:
    """Create a concise text summary of rotation operations."""
    now = datetime.utcnow().isoformat() + "Z"
    summary = f"Rotation audit completed at {now}\\n"
    for s in secrets_status:
        summary += f"Secret {s['name']}, version {s['version']}: {{}}\\n".format(
            "rotated" if s["rotated"] else "failed"
        )
    return summary


# Example usage (will be replaced in production code)
if __name__ == "__main__":
    print(
        rotation_summary(
            [
                {"name": "db-prod", "version": "42", "rotated": True},
                {"name": "api-key", "version": None, "rotated": False},
            ]
        )
    )
