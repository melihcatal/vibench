import json
from storage_client import get_bedrock_runtime_client
from typing import List, Union


def get_embedding_for_text(text_to_embed: Union[str, List[str]]) -> dict:
    """
    Generates an embedding for a given text or list of texts using Amazon Titan Embeddings G1 - Text.
    """
    bedrock_client = get_bedrock_runtime_client()
    model_id = "amazon.titan-embed-text-v1"

    if isinstance(text_to_embed, str):
        body = json.dumps({"inputText": text_to_embed})
    else:
        # This part is for potential batch processing, though the example uses single text
        # For now we will assume a single text input for simplicity
        return {
            "status": "error",
            "message": "List input not supported in this example.",
        }

    try:
        response = bedrock_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
        )
        response_body = json.loads(response.get("body").read())
        embedding = response_body.get("embedding")
        return {"status": "success", "embedding": embedding}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def combine_and_embed_metadata(metadata: dict, extracted_text: str) -> dict:
    """
    Combines object metadata and extracted text into a single string and generates an embedding.
    """
    combined_text = f"Metadata: {json.dumps(metadata)}. Content: {extracted_text}"
    return get_embedding_for_text(combined_text)
