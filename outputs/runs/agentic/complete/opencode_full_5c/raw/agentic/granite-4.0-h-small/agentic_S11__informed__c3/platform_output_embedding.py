# platform_output_embedding.py
# LATER-STEP: generates an embedding for platform model output

from model_client import get_provider_client
from model_models import parse_response


def embed_output(text: str, model_id: str = None) -> list:
    """Produce a vector embedding for the given text using the selected provider's embedding model."""
    provider = infer_provider_name()
    if provider == "aws":
        client = get_provider_client("aws")
        # Amazon Titan Embeddings via Bedrock Runtime
        response = client.invoke_endpoint(
            EndpointName=model_id or "amazon.titan-text-embedding-v1",
            Body=text.encode("utf-8"),
            ContentType="text/plain",
            Accept="application/json",
        )
        payload = json.loads(response["Body"].read())
        return payload["Embedding"]
    elif provider == "azure_openai":
        client = get_provider_client("azure_openai")
        # Azure OpenAI embeddings endpoint
        return client.embeddings.create(
            model=model_id or "text-embedding-ada-002",
            input=text,
        )["data"][0]["embedding"]
    elif provider == "gcp":
        client = get_provider_client("gcp")
        # Vertex AI embeddings
        response = client.embed_content(
            contents=[{"text": text}],
            model=model_id or "textembedding-gecko",
        )
        return response["embeddings"][0]["embedding"]
    elif provider == "hf":
        # Hugging Face text embedding pipeline
        import torch
        from transformers import AutoTokenizer, AutoModel

        tokenizer = AutoTokenizer.from_pretrained(
            "sentence-transformers/all-MiniLM-L6-v2"
        )
        model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        inputs = tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            embeddings = (
                model(**inputs).last_hidden_state.mean(dim=1).squeeze().numpy().tolist()
            )
        return embeddings
    # Add more provider branches as needed
    raise NotImplementedError(f"Embedding not implemented for provider {provider}")
