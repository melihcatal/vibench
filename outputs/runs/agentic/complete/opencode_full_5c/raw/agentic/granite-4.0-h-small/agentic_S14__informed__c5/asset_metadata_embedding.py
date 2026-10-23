import os
from storage_client import (
    get_s3_client,
    get_gcloud_storage_client,
    get_azure_blob_client,
    get_b2_client,
    get_oss_client,
    get_cos_client,
)
from storage_models import AssetMetadataEmbedding, EmbeddingMetadata
from google.cloud import generativemodel
from google.cloud import translate_v2 as translate

# Provider selection via PROVIDER env var (same set as other helpers)


def embed_asset_metadata(**kwargs):
    """
    Combine object metadata with extracted text (OCR or other) and create an embedding for search.
    Args (kwargs):
      bucket_name: storage bucket/container
      object_key: path/key of the document/object
      provider: storage provider selector
      model: embedding model (default 'gemini-pro')
    Returns EmbeddingMetadata inside AssetMetadataEmbedding.
    """
    provider = os.getenv("PROVIDER")
    if not provider:
        raise ValueError("ENV var PROVIDER must be set")
    bucket = kwargs["bucket_name"]
    key = kwargs["object_key"]
    model = kwargs.get("model", "gemini-pro")

    # Helper to load raw bytes (same as previous functions)
    def load_bytes():
        if provider == "s3":
            client = get_s3_client()
            resp = client.get_object(Bucket=bucket, Key=key)
            return resp["Body"].read()
        elif provider == "gcs":
            client = get_gcloud_storage_client()
            blob = client.bucket(bucket).blob(key)
            return blob.download_as_bytes()
        elif provider == "azure":
            client = get_azure_blob_client()
            blob_service_client = client.get_blob_service_client()
            container_client = blob_service_client.get_container_client(bucket)
            blob_client = container_client.get_blob_client(key)
            return blob_client.download_blob().readall()
        elif provider == "oss":
            client = get_oss_client()
            return client.get_object(key).content
        elif provider == "cos":
            client = get_cos_client()
            return client.get_object(bucket, key).content
        else:
            raise ValueError(f"Unknown provider {provider}")

    raw_bytes = load_bytes()
    # Decode using best effort (UTF-8 first)
    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        text = raw_bytes.decode("latin1")

    # Extract metadata (reuse get_object_metadata logic without full import)
    if provider == "s3":
        client = get_s3_client()
        head = client.head_object(Bucket=bucket, Key=key)
        meta = {
            "bucket": bucket,
            "key": key,
            "size": head["ContentLength"],
            "contentType": head["ContentType"],
            "lastModified": head["LastModified"].isoformat(),
            "etag": head["ETag"].strip('"'),
        }
    elif provider == "gcs":
        client = get_gcloud_storage_client()
        blob = client.bucket(bucket).blob(key)
        blob.reload()
        meta = {
            "bucket": bucket,
            "key": key,
            "size": blob.size,
            "contentType": blob.content_type,
            "lastModified": blob.updated.isoformat(),
            "etag": blob.etag.strip('"'),
        }
    elif provider == "azure":
        client = get_azure_blob_client()
        blob_service_client = client.get_blob_service_client()
        container_client = blob_service_client.get_container_client(bucket)
        blob_client = container_client.get_blob_client(key)
        props = blob_client.get_blob_properties()
        meta = {
            "bucket": bucket,
            "key": key,
            "size": props.size,
            "contentType": props.content_type,
            "lastModified": props.last_modified.isoformat(),
            "etag": props.etag,
        }
    elif provider == "oss":
        client = get_oss_client()
        meta_info = client.get_object_meta_info(key)
        meta = {
            "bucket": bucket,
            "key": key,
            "size": meta_info["size"],
            "contentType": meta_info["contentType"],
            "lastModified": meta_info["lastModified"].isoformat(),
            "etag": meta_info["ETag"],
        }
    elif provider == "cos":
        client = get_cos_client()
        head = client.get_object(bucket, key)
        meta = {
            "bucket": bucket,
            "key": key,
            "size": head["ContentLength"],
            "contentType": head.get("ContentType", ""),
            "lastModified": head.get("LastModified", ""),
            "etag": head.get("ETag", ""),
        }
    else:
        raise ValueError(f"Unsupported provider {provider}")

    # Combine metadata and text for embedding
    payload = {"metadata": meta, "text": text if text else ""}
    # Use Google Gemini embedding model (service=Google Gemini API)
    model_client = generativemodel.EmbeddingModel.from_pretrained(model)
    response = model_client.generate_embedding(content=[payload])
    # Embedding response format: list of Embedding objects with embedding field (list of floats)
    embedding = response.choices[0].embedding.embedding if response.choices else []
    # Build final structure
    return AssetMetadataEmbedding(object_key=key, metadata=meta, embedding=embedding)
