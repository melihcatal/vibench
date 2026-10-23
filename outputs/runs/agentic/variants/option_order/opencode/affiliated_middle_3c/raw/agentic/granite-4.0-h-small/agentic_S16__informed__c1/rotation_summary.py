# rotation_summary.py
# Summarizes the status of secret rotation operations across providers.
import json
from typing import List, Dict
from security_models import RotationResult


def summarize_rotations(results: List[RotationResult]) -> str:
    """Produce a markdown summary of secret rotation outcomes."""
    lines = ["# Secret Rotation Summary\n"]
    for i, res in enumerate(results, start=1):
        status = "✅" if res.success else "❌"
        lines.append(f"## Rotation {i}\n")
        lines.append(f"**Status:** {status}\n")
        lines.append(f"**Message:** {res.message}\n")
        lines.append(f"**Version Rotated:** {res.version}\n\n")
    return "".join(lines)


if __name__ == "__main__":
    # Sample usage with dummy data
    demo_results = [
        RotationResult(True, "Secret rotated successfully", 2),
        RotationResult(False, "Version not found", 3),
    ]
    print(summarize_rotations(demo_results))
