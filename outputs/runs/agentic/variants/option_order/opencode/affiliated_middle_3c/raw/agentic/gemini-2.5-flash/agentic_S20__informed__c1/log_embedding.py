import os
import google.generativeai as genai

# Configure the Google Gemini API client for embeddings
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Ensure GOOGLE_API_KEY is set


def embed_log_messages(log_messages: list[str]) -> list[list[float]]:
    """
    Embeds selected log messages for semantic retrieval using the Gemini Embeddings API.
    """
    if not log_messages:
        return []

    # Use a specific Gemini embedding model, e.g., 'embedding-001'
    model = "models/embedding-001"

    try:
        response = genai.embed_content(
            model=model, content=log_messages, task_type="RETRIEVAL_DOCUMENT"
        )
        return [embedding.to_list() for embedding in response["embedding"]]
    except Exception as e:
        print(f"Error embedding log messages: {e}")
        return []


if __name__ == "__main__":
    # Example usage
    log_entries_to_embed = [
        "User authentication failed for user 'johndoe' from IP 192.168.1.1.",
        "Database connection error: Timeout expired.",
        "Successful login for user 'johndoe' from IP 192.168.1.1.",
        "Application started successfully, listening on port 8080.",
    ]

    embeddings = embed_log_messages(log_entries_to_embed)

    if embeddings:
        print(
            f"Generated {len(embeddings)} embeddings. First embedding sample (first 5 elements):\n{embeddings[0][:5]}..."
        )
        # In a real scenario, you would store these embeddings in a vector database
        # for semantic search or similarity comparisons.
    else:
        print("No embeddings were generated.")
