# HELPER
# security_client.py - local configuration and client helper utilities for Secret Management

import os
from google.cloud import secretmanager

# Google Cloud Secret Manager (could be swapped for any provider)

# Configuration options - set via environment variables
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")

# Helper to create a SecretManagerServiceClient with optional custom project


def get_secret_manager_client(
    project_id: str = None,
) -> secretmanager.SecretManagerServiceClient:
    """Return a configured SecretManagerServiceClient.

    Args:
        project_id: Optional Google Cloud project ID. Defaults to env var.

    Returns:
        An authenticated SecretManagerServiceClient instance.
    """
    project = project_id or GOOGLE_CLOUD_PROJECT
    if not project:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT environment variable not set")
    # Client constructor reads credentials from GOOGLE_APPLICATION_CREDENTIALS automatically
    return secretmanager.SecretManagerServiceClient()
