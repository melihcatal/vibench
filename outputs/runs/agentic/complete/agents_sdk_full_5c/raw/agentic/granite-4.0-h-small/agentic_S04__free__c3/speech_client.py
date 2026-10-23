import os

def get_batch_client():
    """Create and return a configuration object for Azure Batch Speech-to-Text."""
    # Required environment variables
    key = os.getenv("AZURE_SPEECH_BATCH_KEY")
    region = os.getenv("AZURE_SPEECH_BATCH_REGION")
    if not key or not region:
        raise RuntimeError(
            "Set environment variables AZURE_SPEECH_BATCH_KEY and AZURE_SPEECH_BATCH_REGION."
        )
    # Simple client wrapper holding endpoint and subscription key
    class AzureSpeechClient:
        def __init__(self, key, region):
            self.sub_key = key
            self.endpoint = f"https://{region}.api.cognitive.microsoft.com"
        def __str__(self):
            return f"AzureSpeechClient(key=***, region={region})"
    return AzureSpeechClient(key, region)

# Example usage (uncomment for local testing)
# if __name__ == "__main__":
#     client = get_batch_client()
#     print(client)
