import boto3
import json
from typing import List
from storage_client import get_bedrock_runtime_client
from storage_models import EmbeddedVector

def embed_text_with_bedrock(text: str, model_id: str = "amazon.titan-embed-text-v1") -> EmbeddedVector:
    """
    Embeds object metadata and extracted text for search using an AWS Bedrock embedding model.
    """
    bedrock_runtime = get_bedrock_runtime_client()

    # The request body depends on the model you are using.
    # This example is for Amazon Titan Embed Text models.
    body = json.dumps({"inputText": text})

    try:
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            contentType='application/json',
            accept='application/json',
            body=body
        )

        response_body = json.loads(response['body'].read())
        # The output key also depends on the model.
        # For Titan Embed Text, it's 'embedding'.
        embedding = response_body.get('embedding')
        
        if not isinstance(embedding, list) or not all(isinstance(x, (int, float)) for x in embedding):
            raise ValueError("Expected embedding to be a list of numbers.")

        return EmbeddedVector(vector=embedding, input_text=text, model_id=model_id)
    except bedrock_runtime.exceptions.ClientError as e:
        print(f"Error invoking Bedrock embedding model: {e}")
        raise

if __name__ == '__main__':
    # Example usage:
    # text_to_embed = "This is a sample document for embedding."
    # try:
    #     # Make sure the specified model ID is enabled in your AWS Bedrock account and region
    #     embedding_result = embed_text_with_bedrock(text_to_embed, model_id="amazon.titan-embed-text-v1")
    #     print(f"Input Text: {embedding_result.input_text}")
    #     print(f"Model Used: {embedding_result.model_id}")
    #     print(f"Embedding (first 5 dimensions): {embedding_result.vector[:5]}...")
    #     print(f"Embedding dimension: {len(embedding_result.vector)}")
    # except Exception as e:
    #     print(f"Embedding failed: {e}")
    pass
