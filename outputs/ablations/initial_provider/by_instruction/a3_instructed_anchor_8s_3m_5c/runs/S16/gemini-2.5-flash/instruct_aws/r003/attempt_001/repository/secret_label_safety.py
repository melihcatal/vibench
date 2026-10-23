import os
import requests
from typing import Dict, Any

def check_text_for_safety(text: str) -> Dict[str, Any]:
    """
    Checks the given text for unsafe content using Azure Content Moderator.

    Args:
        text: The text to be checked.

    Returns:
        A dictionary containing the moderation results.

    Raises:
        ValueError: If AZURE_CONTENT_MODERATOR_ENDPOINT or AZURE_CONTENT_MODERATOR_KEY are not set.
        RuntimeError: For errors during the API call.
    """
    endpoint = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_MODERATOR_KEY")

    if not endpoint:
        raise ValueError("Environment variable AZURE_CONTENT_MODERATOR_ENDPOINT not set.")
    if not key:
        raise ValueError("Environment variable AZURE_CONTENT_MODERATOR_KEY not set.")

    text_moderation_url = f"{endpoint}/contentmoderator/moderate/v1.0/ProcessText/FullText"

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'text/plain',
        'Charset': 'utf-8'
    }

    try:
        response = requests.post(text_moderation_url, headers=headers, data=text.encode('utf-8'))
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error calling Azure Content Moderator API: {e}")

def check_secret_labels_and_notes(labels: str, notes: str) -> Dict[str, Any]:
    """
    Checks secret labels and notes for unsafe text using Azure Content Moderator.

    Args:
        labels: The labels associated with the secret (e.g., comma-separated string).
        notes: The notes associated with the secret.

    Returns:
        A dictionary containing moderation results for both labels and notes.
    """
    results = {
        "labels_moderation": check_text_for_safety(labels) if labels else None,
        "notes_moderation": check_text_for_safety(notes) if notes else None,
    }
    return results
