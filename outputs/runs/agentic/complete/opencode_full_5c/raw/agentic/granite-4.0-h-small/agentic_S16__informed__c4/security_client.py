import os


# Service selection - using Google Secret Manager as the concrete provider
def init_secret_client(service: str = "google") -> any:
    """Initialize a secret management client based on provider selection.

    Args:
        service (str): Provider identifier ('google', 'aws', 'azure', etc.).

    Returns:
        Client object appropriate for the provider.
    """
    if service == "google":
        from google.cloud import secretmanager

        return secretmanager.SecretManagerServiceClient()
    # Placeholder for other providers (not implemented for this task)
    raise NotImplementedError(f"Provider '{service}' not configured for client init")
