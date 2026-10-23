import google.generativeai as genai
import os
from observability_models import EmbeddingRequest, EmbeddingResponse

def embed_log_messages(request: EmbeddingRequest) -> EmbeddingResponse:
    """
    Embeds selected log messages for semantic retrieval using Google's `text-embedding-004` model.

    Args:
        request: An EmbeddingRequest object containing the text (or list of texts) to embed.

    Returns:
        An EmbeddingResponse object with the generated embedding (or list of embeddings).
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('text-embedding-004') # Specify the embedding model

    if isinstance(request.text, str):
        response = model.embed_content(model='text-embedding-004', content=request.text)
        embedding = response['embedding']
    elif isinstance(request.text, list):
        # For batch embedding, the embed_content method handles a list of strings
        response = model.embed_content(model='text-embedding-004', content=request.text)
        embedding = [item['embedding'] for item in response]
    else:
        raise ValueError("Request text must be a string or a list of strings.")

    return EmbeddingResponse(embedding=embedding)

if __name__ == "__main__":
    # Ensure GOOGLE_API_KEY environment variable is set for this example to run
    # os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"

    print("\n--- Embedding Example 1 (Single message) ---")
    single_message_request = EmbeddingRequest(text="Database connection error. Could not reach server on port 5432.")
    try:
        single_embedding_response = embed_log_messages(single_message_request)
        print(f"Original Text: \"{single_message_request.text}\"")
        print(f"Embedding (first 5 elements): {single_embedding_response.embedding[:5]}...")
        print(f"Embedding Length: {len(single_embedding_response.embedding)}")
    except Exception as e:
        print(f"Error embedding single message: {e}")

    print("\n--- Embedding Example 2 (Multiple messages) ---")
    multiple_messages_request = EmbeddingRequest(
        text=[
            "User authentication failed for invalid credentials.",
            "Successful login for administrator user.",
            "Application started on port 8080."
        ]
    )
    try:
        multiple_embedding_response = embed_log_messages(multiple_messages_request)
        print(f"Original Texts: {multiple_messages_request.text}")
        print(f"Number of Embeddings: {len(multiple_embedding_response.embedding)}")
        if multiple_embedding_response.embedding:
            print(f"First Embedding (first 5 elements): {multiple_embedding_response.embedding[0][:5]}...")
            print(f"Length of first embedding: {len(multiple_embedding_response.embedding[0])}")
    except Exception as e:
        print(f"Error embedding multiple messages: {e}")
