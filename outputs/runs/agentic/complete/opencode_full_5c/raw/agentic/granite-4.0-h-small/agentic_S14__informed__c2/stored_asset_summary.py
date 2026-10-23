import os
from typing import Optional
from .storage_client import StorageClient
from .storage_models import GenericObjectMetadata


def summarize_asset(provider: str, bucket: str, key: str) -> str:
    """
    Produce a concise summary of the content stored in an object.

    This function assumes the object contains plain text (e.g., article, report, code).
    It uses a hosted LLM inference service (DashScope Qwen) to generate the summary.
    """
    # Retrieve the object's raw text (simple GET for illustration)
    import requests

    metadata = get_object_metadata(provider, bucket, key)
    url = presigned_download_url(provider, bucket, key)
    resp = requests.get(url)
    resp.raise_for_status()
    content = resp.text

    # Call DashScope Qwen API (example SDK usage)
    import dashscope  # type: ignore[import]

    client = dashscope.ChatClient(api_key=os.getenv("DASHSCOPE_API_KEY"))
    response = client.chat(
        model="qwen",
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following document in 2-3 sentences.\\n\\n{content}",
            }
        ],
    )
    # DashScope returns a JSON with a `choices` list containing `message.content`
    return response.choices[0].message.content  # type: ignore[attr-defined]
