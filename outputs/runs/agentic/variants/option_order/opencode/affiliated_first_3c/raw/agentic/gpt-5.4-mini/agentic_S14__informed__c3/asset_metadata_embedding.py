import openai

from object_metadata import get_object_metadata
from stored_document_ocr import run_document_ocr

EMBEDDING_MODEL = "text-embedding-3-large"


def embed_asset_metadata(bucket: str, key: str, openai_client=None, s3_client=None) -> dict:
    client = openai_client or openai.OpenAI()
    metadata = get_object_metadata(bucket, key, s3_client=s3_client)
    text_result = run_document_ocr(bucket, key, s3_client=s3_client)
    payload = f"bucket={metadata.bucket}
key={metadata.key}
etag={metadata.etag}
content_type={metadata.content_type}
metadata={metadata.metadata}
text={text_result['text']}"
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=payload)
    embedding = response.data[0].embedding if response.data else []
    return {"bucket": bucket, "key": key, "embedding": embedding, "text": text_result["text"], "metadata": metadata.__dict__, "raw": response}
