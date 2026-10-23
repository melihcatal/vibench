import os
import openai
from storage_client import get_s3_client
from storage_models import ObjectMetadata


def summarize_asset(bucket_name: str, object_key: str) -> str:
    """Generate a concise summary of content extracted from a stored asset using OpenAI GPT-4o.

    1. Download the object via S3 client from storage_client.get_s3_client().
    2. Read the full text (assuming UTF-8).
    3. Call OpenAI Chat Completion API to produce a short summary (~2 sentences).
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    s3 = get_s3_client()
    metadata = s3.head_object(Bucket=bucket_name, Key=object_key)
    if "ContentType" not in metadata or not metadata["ContentType"].startswith(
        ("text/plain", "application/pdf")
    ):
        raise ValueError("Object is not plain text or PDF suitable for summarization")

    obj_response = s3.get_object(Bucket=bucket_name, Key=object_key)
    content = obj_response["Body"].read().decode("utf-8")

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following document in two brief sentences:\n\n{content}",
            }
        ],
        temperature=0.2,
        max_tokens=100,
    )
    return response.choices[0].message.content.strip()
