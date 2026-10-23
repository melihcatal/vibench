# stored_asset_summary.py
# [LATER-STEP] Summarizes content extracted from a stored asset (text, images, etc.) using managed LLM service

import json
from google.cloud import storage, vertexai
from storage_client import ManagedStorageClient
from storage_models import ObjectMetadataResponse

# Example: use Vertex AI's LLM for summarization
# The summarizer abstracts provider specifics (model ID, region, etc.)


def summarize_asset(bucket_name: str, blob_name: str) -> json:
    """Generate a concise summary of content stored in an asset/object.

    Args:
        bucket_name (str): Bucket containing the asset.
        blob_name (str): Object/key of the asset (e.g., PDF, markdown).

    Returns:
        JSON string: Summary wrapped in a standardized response.
    """
    # Get a Storage client with authentication
    client = ManagedStorageClient().get_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Download asset content (assumes text-friendly formats; for images/video additional extraction needed)
    asset_content = blob.download_as_text()

    # Set up Vertex AI client and choose a summarization model (e.g., gemini-1.5-flash)
    vertexai.init(project=os.getenv("GOOGLE_CLOUD_PROJECT"), location="us-central1")
    summarizer = vertexai.preview.language_models.ChatModel.from_pretrained(
        "gemini-1.5-flash"
    )

    # Craft prompt for summarization
    prompt = f"Summarize the following document in three sentences.\n\n{asset_content}"

    # Call model and capture the generation
    response = summarizer.predict(prompt)

    # Return structured JSON
    return json.dumps({"summary": response}, indent=2)
