import os
import google.generativeai as genai


def embed_log_message_with_gemini(log_messages: list[str]) -> list:
    """
    Embeds selected log messages for semantic retrieval using the Gemini Embeddings API.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    if not log_messages:
        return []

    try:
        # The embedding model to use
        model_name = "models/embedding-001"

        # Embed the content. The task_type specifies the context for the embeddings.
        # For general text, 'retrieval_document' or 'retrieval_query' are common.
        # 'semantic_similarity' could also be used if the intent is purely similarity comparison.
        result = genai.embed_content(
            model=model_name, content=log_messages, task_type="RETRIEVAL_DOCUMENT"
        )

        embeddings = [embedding["value"] for embedding in result["embeddings"]]

        for i, msg in enumerate(log_messages):
            print(f"Log message: '{msg}' -> Embedding length: {len(embeddings[i])}")

        return embeddings

    except Exception as e:
        print(f"Error embedding log messages with Gemini API: {e}")
        return []


if __name__ == "__main__":
    sample_log_messages = [
        "Database connection timed out after 30 seconds.",
        "Failed to establish connection to the PostgreSQL server.",
        "User 'admin' successfully logged in from IP 192.168.1.10.",
        "Authentication failure for user 'guest'. Invalid credentials.",
        "Disk space low on /var/log, current usage 95%.",
        "Failed to write to persistent storage due to insufficient space.",
    ]

    embeddings = embed_log_message_with_gemini(sample_log_messages)

    if embeddings:
        print(f"Generated {len(embeddings)} embeddings.")
        # You would typically store these embeddings in a vector database
        # for semantic search or similarity comparisons.
    else:
        print("Failed to generate embeddings.")
