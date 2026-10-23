import os
import dashscope  # example provider; replace with actual client as needed


def get_embedder() -> object:
    """Return a configured embedder client using environment credentials.

    Returns:
        object: Configured client instance ready to call embedding endpoints.
    """
    api_key = os.getenv(
        "DASHSCOPE_API_KEY"
    )  # replace with appropriate env var if using another provider
    if not api_key:
        raise RuntimeError("Missing DASHSCOPE_API_KEY environment variable")
    client = dashscope.Embeddings(api_key=api_key)
    return client
