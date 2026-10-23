# Summarize results of an embedding job

import json
from pathlib import Path


def embedding_job_summary(output_path: Path) -> str:
    """Read an embedding job result file and produce a concise summary.

    The file is expected to contain JSON lines where each line is a dict with:
    - 'id': identifier for the text
    - 'embedding': list of floats
    - 'status': 'success' or 'error'
    - 'error_message': optional error text

    Returns a summary string with counts and any errors.
    """
    lines = output_path.read_text().splitlines()
    total = len(lines)
    successes = 0
    errors = []

    for i, line in enumerate(lines, start=1):
        try:
            data = json.loads(line)
            if data.get("status") == "success":
                successes += 1
            else:
                errors.append(f"Line {i}: {data.get('error_message')}")
        except json.JSONDecodeError:
            errors.append(f"Line {i}: invalid JSON")

    summary = (
        f"Embedding job summary for {total} items:\n"
        f"  Successful embeddings: {successes}\n"
        f"  Errors: {len(errors)}"
    )
    if errors:
        summary += ", details:\n" + "\n".join(errors)
    return summary
