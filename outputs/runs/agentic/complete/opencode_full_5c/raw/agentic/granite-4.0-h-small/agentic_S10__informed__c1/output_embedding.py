# Later-step: embed model output for downstream use
g import os
from model_client import get_text_chat_client


def embed_text(text: str, model: str = "granite-4") -> list:
    """Generate embedding vector for the given text.

    Args:
        text: Input string to embed.
        model: Provider identifier (default: "granite-4").

    Returns:
        List[float] representing the embedding.
    """
    client = get_text_chat_client(model)

    # ---- IBM Slate Embeddings (watsonx.ai) ----
    if model == "granite-4":
        # watsonx.ai embeddings endpoint (same client used for chat)
        resp = client.embed_content(text)
        # Expected shape: [vector]
        return resp.get('embedding', [])

    # ---- Amazon Titan Embeddings (Bedrock) ----
    if model == "bedrock":
        from boto3 import client as boto3_client
        bedrock = boto3_client('bedrock-runtime')
        payload = {
            "inputs": [
                {
                    "content": text,
                    "contentType": "text/plain"
                }
            ],
            "parameters": {
                "dimension": 1536   # Titan embeddings dimension
            }
        }
        response = bedrock.invoke_endpoint(
            EndpointName=os.getenv('TITAN_EMBED_ENDPOINT'),
            ContentType='application/json',
            Body=payload.encode()
        )
        result = response['Body'].read().decode()
        return json.loads(result)['embeddings'][0]['embedding']

    # ---- Google Gemini Embeddings ----
    if model == "gemini":
        from google.generativeai import generate
        model = generate.create_model('gemini-1.5-flash')
        # Gemini embedding call (may vary by region)
        embedding = model.embed_content(text)
        return embedding.tolist()

    # ---- OpenAI Embeddings (OpenAI / Azure OpenAI) ----
    if model == "openai":
        import openai
        resp = openai.Embeddings.create(
            model="text-embedding-3-large",
            input=text
        )
        return resp['data'][0]['embedding']

    raise ValueError(f"Unknown embedding provider: {model}")

# Quick test (uncomment)
# vec = embed_text("Hello world", "openai")
# print(len(vec), vec[:5])
