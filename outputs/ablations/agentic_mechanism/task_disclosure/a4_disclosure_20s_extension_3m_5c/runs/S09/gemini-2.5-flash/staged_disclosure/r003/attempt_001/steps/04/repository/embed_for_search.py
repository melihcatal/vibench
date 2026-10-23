import os
import openai

def embed_text(text_to_embed: str):
    """Embeds a given text using OpenAI's text-embedding-ada-002 model."""
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=text_to_embed
    )
    return response.data[0].embedding

def embed_query(query: str):
    """Embeds a search query."""
    return embed_text(query)

def embed_documents(documents: list[str]):
    """Embeds a list of documents."""
    return [embed_text(doc) for doc in documents]

if __name__ == "__main__":
    # Example Usage
    query = "What is the capital of France?"
    documents = [
        "Paris is the capital and most populous city of France.",
        "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris.",
        "Berlin is the capital of Germany."
    ]

    query_embedding = embed_query(query)
    print(f"Query embedding (first 5 dimensions): {query_embedding[:5]}...")

    document_embeddings = embed_documents(documents)
    print(f"Document 1 embedding (first 5 dimensions): {document_embeddings[0][:5]}...")
    print(f"Document 2 embedding (first 5 dimensions): {document_embeddings[1][:5]}...")
    print(f"Document 3 embedding (first 5 dimensions): {document_embeddings[2][:5]}...")
