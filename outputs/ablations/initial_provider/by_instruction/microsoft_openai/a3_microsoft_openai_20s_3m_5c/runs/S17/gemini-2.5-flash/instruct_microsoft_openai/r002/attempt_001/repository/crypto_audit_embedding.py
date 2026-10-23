import os
import argparse
from security_client import SecurityClient
from security_models import EmbeddingRequest, EmbeddingResponse

def crypto_audit_embedding_main():
    parser = argparse.ArgumentParser(description="Embed crypto audit notes for semantic search using Azure OpenAI.")
    parser.add_argument("--note", required=True, help="The crypto audit note to embed.")
    parser.add_argument("--model-name", default="text-embedding-ada-002", 
                        help="The deployment name of the embedding model in Azure OpenAI.")
    parser.add_argument("--azure-openai-endpoint", required=False, 
                        help="The Azure OpenAI endpoint. Defaults to AZURE_OPENAI_ENDPOINT environment variable.")
    parser.add_argument("--azure-openai-api-key", required=False, 
                        help="The Azure OpenAI API key. Defaults to AZURE_OPENAI_API_KEY environment variable.")

    args = parser.parse_args()

    azure_openai_endpoint = args.azure_openai_endpoint or os.environ.get("AZURE_OPENAI_ENDPOINT")
    azure_openai_api_key = args.azure_openai_api_key or os.environ.get("AZURE_OPENAI_API_KEY")

    if not azure_openai_endpoint or not azure_openai_api_key:
        raise ValueError("Azure OpenAI endpoint and API key not provided. Please set relevant arguments or environment variables.")

    client = SecurityClient()
    request = EmbeddingRequest(text=args.note, model=args.model_name)

    try:
        response: EmbeddingResponse = client.create_embedding(request)
        print(f"Embedding created successfully for the audit note (first 10 dimensions): {response.embedding[:10]}...")
        print(f"Embedding dimension: {len(response.embedding)}")
    except Exception as e:
        print(f"Embedding creation failed: {e}")

if __name__ == "__main__":
    crypto_audit_embedding_main()
