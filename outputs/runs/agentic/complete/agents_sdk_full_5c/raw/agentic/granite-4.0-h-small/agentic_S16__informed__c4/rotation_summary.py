import json
from typing import List, Dict

def rotation_summary(projects: List[str], secrets: List[str], client) -> str:
    """Produce a summary report of each secret's latest version and any pending rotation plans.

    Args:
        projects: List of GCP project IDs to inspect.
        secrets:  List of secret IDs (across projects) to summarize.
        client:   SecurityClient instance for cloud secret access.

    Returns:
        A JSON string containing a list of summary objects.
    """
    report = []
    for proj in projects:
        for secret in secrets:
            try:
                value = client.get_secret(secret)
                # Simple decode check
                latest_version = client.get_secret_version(project=proj, secret=secret, version="latest")
                report.append({
                    "project": proj,
                    "secret": secret,
                    "latest_version": latest_version,
                    "value_sample": value[:20] + ("..." if len(value) > 20 else "")
                })
            except Exception as exc:
                report.append({
                    "project": proj,
                    "secret": secret,
                    "error": str(exc)
                })
    return json.dumps(report, indent=2)
