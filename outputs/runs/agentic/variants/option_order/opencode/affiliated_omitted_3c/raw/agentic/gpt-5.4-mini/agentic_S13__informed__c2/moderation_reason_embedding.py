import cohere


def moderation_reason_embedding(text: str):
    client = cohere.Client()
    response = client.embed(
        texts=[text], model="embed-english-v3.0", input_type="search_document"
    )
    return response.embeddings[0]
