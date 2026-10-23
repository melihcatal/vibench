from embeddings_client import embed_text_google, embed_texts_google


def embed_for_search(query: str, documents):
    return {
        "query_embedding": embed_text_google(query),
        "document_embeddings": embed_texts_google(documents),
    }
