import openai
import os
from storage_client import get_s3_client


def embed_asset_metadata_and_text(bucket: str, key: str) -> list[float]:
    s3_client = get_s3_client()
    metadata_response = s3_client.head_object(Bucket=bucket, Key=key)
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    text = obj["Body"].read().decode("utf-8")
    metadata_str = str(
        {
            k: v
            for k, v in metadata_response.items()
            if k in ["ContentLength", "ContentType", "LastModified", "ETag"]
        }
    )
    combined = f"Metadata: {metadata_str}\nText: {text}"
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(input=combined, model="text-embedding-3-small")
    return response.data[0].embedding
