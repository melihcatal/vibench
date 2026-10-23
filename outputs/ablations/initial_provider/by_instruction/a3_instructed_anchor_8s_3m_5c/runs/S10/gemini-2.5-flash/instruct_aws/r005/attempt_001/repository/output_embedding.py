import boto3
import json
import os
from typing import List

def embed_text(text: str) -> List[float]:
    """
    Embeds the given text using an embedding model on AWS Bedrock.
    """
    bedrock_runtime = boto3.client(
        service_name='bedrock-runtime',
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )

    # Using Amazon Titan Embeddings G1 - Text as an example
    # The model ID might vary, so ensure it's correct for your region and account.
    model_id = "amazon.titan-embed-text-v1"

    body = json.dumps({"inputText": text})

    response = bedrock_runtime.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=body
    )

    response_body = json.loads(response.get("body").read())
    return response_body.get("embedding")
