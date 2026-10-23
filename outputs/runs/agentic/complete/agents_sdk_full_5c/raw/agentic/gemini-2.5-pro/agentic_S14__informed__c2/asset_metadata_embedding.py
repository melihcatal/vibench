import boto3
import json
import os
from typing import List, Dict, Any

from storage_models import ObjectMetadata


def embed_metadata_and_text(
    metadata: ObjectMetadata, text_content: str
) -> List[float]:
    """
    Creates a text embedding for an asset's metadata and content using Amazon Titan Embeddings.

    :param metadata: An ObjectMetadata object for the asset.
    :param text_content: The extracted text content of the asset.
    :return: A list of floats representing the embedding vector.
    """
    # Provider: Amazon Bedrock
    # Model Family: Amazon Titan
    model_id = "amazon.titan-embed-text-v1"

    bedrock_runtime_client = boto3.client(
        "bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    # Combine metadata and text into a single input string for embedding
    metadata_str = (
        f"Key: {metadata.object_key}, "
        f"Type: {metadata.content_type}, "
        f"Size: {metadata.content_length} bytes. "
    )
    if metadata.custom_metadata:
        meta_items = ", ".join(f"{k}:{v}" for k, v in metadata.custom_metadata.items())
        metadata_str += f"Custom Metadata: ({meta_items})."

    combined_text = f"METADATA: {metadata_str}\n\nCONTENT: {text_content}"

    request_body = {"inputText": combined_text}

    try:
        response = bedrock_runtime_client.invoke_model(
            body=json.dumps(request_body),
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
        )
        response_body = json.loads(response["body"].read())
        embedding = response_body.get("embedding")
        if embedding:
            return embedding
        else:
            print("Error: Embedding not found in the response.")
            return []
    except Exception as e:
        print(f"An error occurred during embedding creation: {e}")
        return []
