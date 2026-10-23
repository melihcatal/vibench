import os
import boto3
import json
import tempfile
from google.cloud import genai  # Assuming same-scenario Google Cloud Storage
from google.cloud import storage
from storage_client import ManagedObjectStorageClient


def embed_asset_metadata(
    bucket: str, key: str, prompt: str = "Summarize the metadata for search"
) -> dict:
    """Create a vector embedding that combines object metadata and extracted text for search.

    Parameters:
        bucket (str): Bucket name.
        key (str): Object key/path.
        prompt (str): Optional LLM prompt to guide embedding generation.

    Returns:
        dict: Embedding result containing a vector ID and the vector data.
    """
    # 1️⃣ Load object metadata via S3 HEAD
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    metadata = s3_client.head_object(Bucket=bucket, Key=key)

    # 2️⃣ Load extracted text if available (assumes a `metadata.json` sibling or a separate object)
    # For illustration, we read a JSON side‑car file `metadata.json` in the same bucket.
    try:
        txt_obj = (
            boto3.resource("s3")
            .Object(bucket, key.replace(".pdf", "_metadata.json"))
            .get()
        )
        extracted_text = txt_obj["Body"].read().decode("utf-8")
    except Exception:
        extracted_text = ""

    # 3️⃣ Combine metadata JSON and extracted text into a single string
    combined = json.dumps(metadata) + "\n" + extracted_text

    # 4️⃣ Generate an embedding via Google Gemini (or any LLM with embeddings)
    # Set up Gemini client with GOOGLE_API_KEY env variable
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GeminiModel()
    # Use a tool that returns embeddings (Gemini 1.5 supports embeddings)
    embedding_response = model.embed_content(combined, model="gemini-1.5-flash")

    # 5️⃣ Return the embedding vector (as list of floats) and the vector ID
    embedding = embedding_response.candidates[0].embedding_content
    # Gemini returns a list of floats; convert to plain list
    vector = list(embedding.data)
    return {"embeddingId": embedding.id, "vector": vector, "metadata": metadata}
