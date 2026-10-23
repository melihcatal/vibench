# [HELPER] speech_client.py
# Local utilities for configuring and authenticating Batch Speech-to-Text requests
import os


def get_auth_header(service: str = None) -> dict:
    """
        Return an authentication header appropriate for the given provider.

        service: identifier string for the provider (optional). If omitted, expects environment variables
    to be set per the default provider used in the same-scenario scripts (AssemblyAI).

        Returns a dict suitable for HTTP Authorization headers, or raises if no suitable credentials are found.
    """
    # Define mapping from service name to expected env vars
    env_map = {
        "AssemblyAI": ("ASSEMBLYAI_API_KEY",),
        "Azure AI Speech": ("AZURE_SPEECH_KEY", "AZURE_SPEECH_REGION"),
        "Google Cloud Speech": ("GOOGLE_APPLICATION_CREDENTIALS",),
        "AWS Transcribe": ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"),
    }
    if service:
        creds = env_map.get(service)
        if not creds:
            raise ValueError(f"Unsupported service for auth: {service}")
        missing = [c for c in creds if not os.getenv(c)]
        if missing:
            raise RuntimeError(
                f"Missing environment variables for {service}: {', '.join(missing)}"
            )
        # Simple example for services that accept Bearer token (AssemblyAI, Azure)
        if service in ("AssemblyAI", "Azure AI Speech"):
            return {"authorization": os.getenv(creds[0])}
        # For Google we use Application Default Credentials via google-auth library
        if service == "Google Cloud Speech":
            from google.auth import default

            creds, _ = default()
            return {"authorization": f"Bearer {creds.token}"}
        # AWS example assumes signing via botocore; here we just return a placeholder header
        return {"x-amz-access-key": os.getenv(creds[0])}
    # Fallback: use AssemblyAI default (expects ASSEMBLYAI_API_KEY)
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "No authentication credentials found. Set ASSEMBLYAI_API_KEY or provide service parameter."
        )
    return {"authorization": api_key}
