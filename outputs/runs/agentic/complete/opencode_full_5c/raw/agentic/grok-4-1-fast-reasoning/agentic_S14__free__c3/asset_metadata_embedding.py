from openai import OpenAI
import os
from storage_client import get_s3_client
from typing import List


def asset_metadata_embedding(bucket: str, key: str) -> List[float]:
    s3_client = get_s3_client()
    head_response = s3_client.head_object(Bucket=bucket, Key=key)
    meta_str = f"ContentLength: {head_response['ContentLength']}, ContentType: {head_response['ContentType']}"
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    content = obj["Body"].read().decode("utf-8")[:8000]
    text = meta_str + "\n" + content
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return [float(x) for x in response.data[0].embedding]
