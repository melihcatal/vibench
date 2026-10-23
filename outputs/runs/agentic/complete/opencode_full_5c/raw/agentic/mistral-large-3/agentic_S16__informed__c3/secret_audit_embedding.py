import os
import boto3
from security_models import EmbeddingRequest, EmbeddingResponse


def secret_audit_embedding(text: str) -> EmbeddingResponse:
    client = boto3.client(
        service_name="bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1")
    )

    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body=bytes(f'{{"inputText": "{text}"}}', "utf-8"),
    )

    result = eval(response["body"].read().decode("utf-8"))
    return EmbeddingResponse(
        embedding=result["embedding"], model_id="amazon.titan-embed-text-v1"
    )
