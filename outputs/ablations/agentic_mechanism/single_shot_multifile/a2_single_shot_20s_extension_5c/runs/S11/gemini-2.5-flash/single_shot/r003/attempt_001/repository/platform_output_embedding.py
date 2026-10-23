import json
import os
from model_client import get_bedrock_runtime_client
from model_models import parse_titan_embedding_response

def get_text_embedding(text: str, model_id: str = "amazon.titan-embed-text-v1") -> list[float]:
    bedrock_runtime = get_bedrock_runtime_client()
    
    body = json.dumps({"inputText": text})

    response = bedrock_runtime.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=body
    )

    response_body = response["body"].read().decode("utf-8")
    return parse_titan_embedding_response(response_body)
