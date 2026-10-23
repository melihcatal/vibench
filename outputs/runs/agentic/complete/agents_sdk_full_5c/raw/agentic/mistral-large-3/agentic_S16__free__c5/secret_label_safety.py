import os
import requests
from typing import Dict, List


def check_secret_labels_for_unsafe_text(secret_labels: Dict[str, str]) -> List[Dict[str, str]]:
    """
    Checks secret labels and notes for unsafe text using GitHub's Secret Scanning API.
    
    Args:
        secret_labels: A dictionary of secret labels/notes (e.g., {"label": "value"}).
    
    Returns:
        A list of findings with unsafe text and their locations.
    """
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is required.")
    
    url = "https://api.github.com/repos/github/example-secret-scanning/secret-scanning/verify"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    
    findings = []
    for label, value in secret_labels.items():
        payload = {"secret": value}
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200 and response.json().get("matches"):
            findings.append({
                "label": label,
                "value": value,
                "message": "Unsafe text detected.",
            })
    
    return findings