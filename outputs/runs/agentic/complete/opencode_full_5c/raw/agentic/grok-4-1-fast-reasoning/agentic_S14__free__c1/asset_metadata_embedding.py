import openai
import os
from storage_client import get_storage_client
from object_metadata import get_object_metadata
from typing import List


def create_asset_embedding(bucket: str, object_key: str) -> List[float]:
    openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    metadata = get_object_metadata(bucket, object_key)
    s3_client = get_storage_client()
    response = s3_client.get_object(Bucket=bucket, Key=object_key)
    text = response["Body"].read().decode("utf-8", errors="ignore")[:8000]
    combined_text = f"Metadata: {metadata}\nContent: {text}"
    embedding_response = openai_client.embeddings.create(
        model="text-embedding-3-small", input=combined_text
    )
    return embedding_response.data[0].embedding
