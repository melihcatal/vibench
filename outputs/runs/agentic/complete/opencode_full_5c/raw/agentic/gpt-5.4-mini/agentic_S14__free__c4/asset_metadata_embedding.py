from openai import OpenAI

from storage_client import get_bucket_name, get_object_key, get_s3_client


def asset_metadata_embedding(bucket=None, key=None):
    s3 = get_s3_client()
    head = s3.head_object(Bucket=get_bucket_name(bucket), Key=get_object_key(key))
    text = " ".join(
        [f"{k}:{v}" for k, v in head.items() if isinstance(v, (str, int, float))]
    )
    client = OpenAI()
    return (
        client.embeddings.create(model="text-embedding-3-large", input=text)
        .data[0]
        .embedding
    )
