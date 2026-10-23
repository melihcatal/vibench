from cohere import Cohere


def embed_caption_chunks(chunks: list[str]) -> list[list[float]]:
    client = Cohere()
    result = client.embed(
        texts=chunks, model="embed-english-v3.0", input_type="search_document"
    )
    return result.embeddings
