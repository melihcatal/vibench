import anthropic
from storage_client import StorageClient


def summarize_stored_asset(bucket: str, key: str, prompt: str) -> str:
    """Summarize content extracted from a stored asset using Anthropic Claude."""
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # Download the asset from IBM COS
    storage_client = StorageClient().get_client()
    response = storage_client.get_object(Bucket=bucket, Key=key)
    text = response["Body"].read().decode("utf-8")
    
    # Summarize using Anthropic
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        messages=[{"role": "user", "content": f"{prompt}\n\n{text}"}],
    )
    return message.content[0].text