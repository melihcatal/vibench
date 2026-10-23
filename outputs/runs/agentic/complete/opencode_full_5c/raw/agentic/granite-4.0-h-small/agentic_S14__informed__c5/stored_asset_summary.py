import os
from storage_client import (
    get_s3_client,
    get_gcloud_storage_client,
    get_azure_blob_client,
    get_b2_client,
    get_oss_client,
    get_cos_client,
)
from storage_models import AssetSummary
from google.cloud import generativemodel
from typing import Optional

# Provider selected via PROVIDER env var (same set as other helpers)


def summarize_asset(**kwargs):
    """
    Summarize the extracted text of a stored asset using a hosted LLM.
    Args (kwargs):
      bucket_name: storage bucket/container
      object_key: path/key of the document/object
      provider: storage provider selector
      model: optional LLM model identifier (defaults to Gemini 'gemini-1.5-flash')
    Returns AssetSummary containing .summary.
    """
    provider = os.getenv("PROVIDER")
    if not provider:
        raise ValueError("ENV var PROVIDER must be set")
    bucket = kwargs["bucket_name"]
    key = kwargs["object_key"]
    model = kwargs.get("model", "gemini-1.5-flash")

    # Load asset text (reuse extraction logic)
    def load_text():
        if provider == "s3":
            client = get_s3_client()
            response = client.get_object(Bucket=bucket, Key=key)
            return response["Body"].read()
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

    raw_bytes = load_text()
    # Attempt to decode as utf-8; fallback to bytes.decode('latin1')
    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        text = raw_bytes.decode("latin1")

    # Use Google Gemini API for summarization (service=Google Gemini API)
    model_client = generativemodel.ChatModel.from_pretrained(model)
    response = model_client.predict(
        messages=[
            {
                "role": "user",
                "parts": [
                    {
                        "text": f"You are an AI assistant. Please read the following document and produce a concise summary (max 150 words). Document:\n\n{text}\n\nProvide the summary as plain text only, no extra comments."
                    }
                ],
            }
        ],
    )
    # response.choices[0].message.content holds the LLM output
    summary = response.choices[0].message.content.strip() if response.choices else ""
    return AssetSummary(summary=summary)
