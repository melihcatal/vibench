from typing import Dict, List
import numpy as np
from storage_client import StorageClient


def asset_metadata_embedding(
    bucket_name: str, object_key: str, extracted_text: str = None
) -> List[float]:
    """
    Embeds object metadata and extracted text from Amazon S3 using AWS Bedrock Titan Embeddings.
    """
    client = StorageClient().get_client()

    try:
        # Fetch object metadata
        metadata_response = client.head_object(Bucket=bucket_name, Key=object_key)

        # Prepare metadata text for embedding
        metadata_text = " ".join(
            [f"{k}: {v}" for k, v in metadata_response.get("Metadata", {}).items()]
        )

        # Combine metadata and extracted text
        combined_text = f"Metadata: {metadata_text}"
        if extracted_text:
            combined_text += f" Extracted Text: {extracted_text}"

        # Call AWS Bedrock for embeddings (using Titan Embeddings model)
        bedrock_client = client("bedrock-runtime", region_name="us-east-1")
        bedrock_response = bedrock_client.invoke_model(
            modelId="amazon.titan-embed-text-v1",
            body=bytes(f'{{"inputText":"{combined_text}"}}', "utf-8"),
        )

        # Parse the response
        response_body = bedrock_response["body"].read().decode("utf-8")
        embedding = np.array(eval(response_body.split('"embedding":')[1].split("}")[0]))

        return embedding.tolist()
    except Exception as e:
        raise Exception(f"Failed to generate embedding for S3 object: {str(e)}")
