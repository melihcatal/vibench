import boto3
import json
from typing import List
from storage_client import get_bedrock_runtime_client
from storage_models import EmbedTextRequest, EmbedTextResponse

def embed_asset_metadata_and_text(request: EmbedTextRequest) -> EmbedTextResponse:
    """
    Embeds object metadata and extracted text for search using Amazon Bedrock.
    This example uses a common embedding model like 'amazon.titan-embed-text-v1'.
    """
    bedrock_runtime_client = get_bedrock_runtime_client()
    
    # The model ID for Amazon Titan Embeddings G1 - Text
    # This is a concrete provider-specific model identifier.
    model_id = 'amazon.titan-embed-text-v1' 

    try:
        body = json.dumps({"inputText": request.text})
        
        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )
        
        response_body = json.loads(response.get('body').read())
        embedding = response_body.get('embedding')
        
        if embedding:
            return EmbedTextResponse(success=True, embedding=embedding, message="Text successfully embedded.")
        else:
            return EmbedTextResponse(success=False, message="No embedding found in the model response.")
            
    except bedrock_runtime_client.exceptions.ValidationException as e:
        return EmbedTextResponse(success=False, message=f"Bedrock validation error: {e}")
    except bedrock_runtime_client.exceptions.ModelErrorException as e:
        return EmbedTextResponse(success=False, message=f"Bedrock model error: {e}")
    except Exception as e:
        return EmbedTextResponse(success=False, message=f"An unexpected error occurred during embedding: {e}")

