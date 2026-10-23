import os
from typing import Dict, Any
from googleapiclient import discovery
from google.oauth2 import service_account

_GOOGLE_SAFETY_API_KEY = os.getenv("GOOGLE_SAFETY_API_KEY")
_GOOGLE_SAFETY_CREDENTIALS = os.getenv("GOOGLE_SAFETY_CREDENTIALS_JSON")


def check_prompt_safety(text: str) -> Dict[str, Any]:
    """
    Check prompts and generated text for unsafe content using Google Cloud's Natural Language API.
    """
    if not _GOOGLE_SAFETY_API_KEY and not _GOOGLE_SAFETY_CREDENTIALS:
        raise ValueError("Either GOOGLE_SAFETY_API_KEY or GOOGLE_SAFETY_CREDENTIALS_JSON must be set.")

    credentials = None
    if _GOOGLE_SAFETY_CREDENTIALS:
        credentials = service_account.Credentials.from_service_account_info(
            info=_GOOGLE_SAFETY_CREDENTIALS
        )

    client = discovery.build(
        "commentanalyzer", 
        "v1alpha1", 
        developerKey=_GOOGLE_SAFETY_API_KEY,
        credentials=credentials
    )

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        }
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response