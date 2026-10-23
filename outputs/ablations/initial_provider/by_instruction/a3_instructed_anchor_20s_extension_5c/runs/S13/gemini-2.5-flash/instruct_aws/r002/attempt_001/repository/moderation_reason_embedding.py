import os
import cohere

def moderation_reason_embedding(reason_text: str) -> dict:
    """
    Embed moderation rationales for case retrieval using Cohere API.
    """
    cohere_api_key = os.environ.get("COHERE_API_KEY")

    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(cohere_api_key)

    try:
        response = co.embed(
            texts=[reason_text],
            model='embed-english-v3.0',  # Or other appropriate Cohere embedding model
            input_type='search_document' # Or 'search_query', 'classification', 'clustering'
        )

        embedding = response.embeddings[0]

        return {
            "original_text": reason_text,
            "embedding": embedding,
            "model": 'embed-english-v3.0',
            "raw_cohere_response": response.to_dict() # Convert to dict for easier handling
        }
    except cohere.CohereError as e:
        return {"error": str(e), "message": "Failed to get embedding from Cohere API."}
