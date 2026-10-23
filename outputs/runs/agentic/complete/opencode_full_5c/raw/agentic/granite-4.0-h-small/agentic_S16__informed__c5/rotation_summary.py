import json
from pathlib import Path


def summarize_rotation_status(rotations: list[dict]) -> str:
    """Summarize rotation status for multiple secrets.

    Each rotation entry should contain 'secret_id' and 'status'.
    Returns a concise markdown string.
    """
    lines = [f"# Secret Rotation Summary"]
    for entry in rotations:
        lines.append(
            f"- {entry['secret_id']}: {entry['status']} ({entry.get('message', '')})"
        )
    return "\\n".join(lines)


if __name__ == "__main__":
    # Example usage with JSON file input
    data = json.loads(Path("rotation_log.json").read_text())
    print(summarize_rotation_status(data))
