from typing import Any, Dict, List

from openai import OpenAI

from storage_client import create_s3_client, get_storage_config


def asset_metadata_embedding(bucket: str, key: str, extra_text: str = "") -> Dict[str, Any]:
    config = get_storage_config()
    s3_client = create_s3_client(config)
    obj = s3_client.head_object(Bucket=bucket, Key=key)
    metadata = obj.get("Metadata", {})
    parts = [f"bucket:{bucket}", f"key:{key}"] + [f"{k}:{v}" for k, v in metadata.items()]
    if extra_text:
        parts.append(extra_text)
    text = "\n".join(parts)
    client = OpenAI()
    embedding = client.embeddings.create(model="text-embedding-3-small", input=text)
    vector = embedding.data[0].embedding if embedding.data else []
    return {"bucket": bucket, "key": key, "text": text, "embedding": vector, "dimension": len(vector)}
