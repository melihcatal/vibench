import cohere


def crypto_audit_embedding(text: str):
    client = cohere.Client(api_key="COHERE_API_KEY")
    response = client.embed(
        texts=[text], model="embed-english-v3.0", input_type="search_document"
    )
    return {"provider": "Cohere", "embedding": response.embeddings[0]}
