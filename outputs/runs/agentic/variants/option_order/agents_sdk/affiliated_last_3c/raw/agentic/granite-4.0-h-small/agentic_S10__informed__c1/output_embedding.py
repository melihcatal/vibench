import os
from model_client import normalize_response, get_llm_client
from model_models import RequestShape

# Use Amazon Titan embeddings via Bedrock Runtime (boto3)
import boto3

bedrock_runtime = boto3.client('bedrock-runtime')
# Model ID for Titan Text Embedding (us-east-1 region)
TITAN_EMBED_MODEL = "anthropic.claude-3-5-sonnet-20240620-v1:0"

BEDROCK_ENDPOINT = os.getenv(
    "BEDROCK_RUNTIME_ENDPOINT", "https://bedrock.us-east-1.amazonaws.com"
)
if not BEDROCK_ENDPOINT:
    raise RuntimeError("Set BEDROCK_RUNTIME_ENDPOINT environment variable")

bedrock_runtime.endpoint_url = BEDROCK_ENDPOINT


def embed_text(text: str) -> List[float]:
    """Generate embedding for a single piece of text using Amazon Titan.

    Returns a list of float values representing the embedding vector.
    """
    payload = {
        "inputs": [
            {
                "text": text
            }
        ],
        "parameters": {
            "contentType": "application/json"
        }
    }
    response = bedrock_runtime
        .invoke_model(
            ModelId=TITAN_EMBED_MODEL,
            ContentType="application/json",
            Body=bytes(json.dumps(payload), encoding='utf-8')
        )
    # Bedrock returns a JSON body like {"outputs": [{"embedding": [0.01, ...]}]}
    body = response.get('Body')
    if body is None:
        raise RuntimeError("Bedrock response missing body")
    result = json.load(body)
    embedding = result.get('outputs', [{}])[0].get('embedding')
    if not embedding:
        raise RuntimeError("Embedding not found in response")
    return embedding


def embed_response(response: RequestShape) -> RequestShape:
    """Add an embedding field to the LLM response based on its generated text.

    The embedding is computed on the assistant's content.
    
    Args:
        response (RequestShape): Normalized LLM response.
    
    Returns:
        RequestShape: Same dict with an added \"embedding\" key under the assistant message.
    """
    if response.get("choices"):
        content = response["choices"][0]["message"].get("content", "")
        embedding = embed_text(content)
        # Insert embedding alongside the content (optional for downstream tasks)
        response["choices"][0]["message"]["embedding"] = embedding
    return response
