"""Embed object metadata and extracted text for search using Amazon Bedrock Titan.

Uses boto3 to call the AWS Bedrock embedding model
(amazon.titan-embed-text-v2:0) to generate vector embeddings from
object metadata and extracted text content.
Requires AWS credentials in environment variables:
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
"""

import json
from storage_client import get_s3_client, get_textract_client
from storage_models import AssetEmbedding
from stored_document_ocr import stored_document_ocr

BEDROCK_EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v2:0"


def _invoke_bedrock_embedding(text, region=None):
    """Call AWS Bedrock Titan embedding model to generate a vector.

    Args:
        text: Input text to embed.
        region: AWS region for Bedrock.

    Returns:
        List of floats representing the embedding vector.
    """
    import boto3

    bedrock_region = region or "us-east-1"

    session = boto3.Session(
        aws_access_key_id=__import__("os").environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=__import__("os").environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=bedrock_region,
    )
    bedrock_runtime = session.client("bedrock-runtime", region_name=bedrock_region)

    body = json.dumps({
        "inputText": text,
        "dimensions": 1024,
        "normalize": True,
    })

    response = bedrock_runtime.invoke_model(
        modelId=BEDROCK_EMBEDDING_MODEL_ID,
        body=body,
    )

    result_body = json.loads(response["body"].read())
    return result_body["embedding"]


def asset_metadata_embedding(bucket, key, region=None, s3_endpoint_url=None,
                             include_text=True):
    """Generate embeddings for an S3 object's metadata and extracted text.

    Downloads the object metadata and optionally extracts text via Textract OCR,
    then generates separate and combined embeddings using the
    amazon.titan-embed-text-v2:0 model on AWS Bedrock.

    Args:
        bucket: S3 bucket name.
        key: S3 object key.
        region: Optional AWS region override.
        s3_endpoint_url: Optional custom S3 endpoint.
        include_text: Whether to also embed extracted text content.

    Returns:
        AssetEmbedding with metadata_vector, text_vector, and combined_vector.
    """
    object_uri = f"s3://{bucket}/{key}"

    # Step 1: Gather metadata
    s3_client = get_s3_client(region=region, endpoint_url=s3_endpoint_url)
    head_response = s3_client.head_object(Bucket=bucket, Key=key)
    content_type = head_response.get("ContentType", "unknown")
    content_length = head_response.get("ContentLength", 0)
    user_metadata = head_response.get("Metadata", {})

    metadata_str = (
        f"content_type: {content_type}, "
        f"size: {content_length} bytes, "
        f"user_metadata: {json.dumps(user_metadata)}"
    )

    metadata_vector = _invoke_bedrock_embedding(metadata_str, region=region)

    text_vector = []
    combined_vector = []

    if include_text:
        # Step 2: Extract text via Textract OCR
        try:
            ocr_result = stored_document_ocr(bucket, key, region=region)
            extracted_text = ocr_result.text
        except Exception:
            # Fallback: try reading object body as text
            try:
                get_response = s3_client.get_object(Bucket=bucket, Key=key)
                extracted_text = get_response["Body"].read().decode("utf-8", errors="replace")
            except Exception:
                extracted_text = ""

        if extracted_text:
            text_vector = _invoke_bedrock_embedding(extracted_text, region=region)

            # Step 3: Generate combined embedding
            combined_text = f"{metadata_str}\n---\n{extracted_text}"
            combined_vector = _invoke_bedrock_embedding(combined_text, region=region)

    return AssetEmbedding(
        object_uri=object_uri,
        metadata_vector=metadata_vector,
        text_vector=text_vector,
        combined_vector=combined_vector,
        model_name=BEDROCK_EMBEDDING_MODEL_ID,
        dimensions=1024,
    )


def embedding_for_text(text, object_uri=None, region=None):
    """Generate a single embedding vector for arbitrary text.

    Args:
        text: Text content to embed.
        object_uri: Optional S3 URI for provenance tracking.
        region: Optional AWS region override.

    Returns:
        AssetEmbedding with the text embedding vector.
    """
    vector = _invoke_bedrock_embedding(text, region=region)

    return AssetEmbedding(
        object_uri=object_uri or "unknown",
        metadata_vector=[],
        text_vector=vector,
        combined_vector=vector,
        model_name=BEDROCK_EMBEDDING_MODEL_ID,
        dimensions=1024,
    )
