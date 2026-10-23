import google.generativeai as genai
import os


def embed_log_messages(log_messages):
    """
    Embeds selected log messages for semantic retrieval using Gemini Embeddings.
    `log_messages` should be a list of strings.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    embeddings = genai.embed_content(
        model="models/embedding-001",
        content=log_messages,
        task_type="RETRIEVAL_DOCUMENT",  # or "SEMANTIC_SIMILARITY", "AQA_QUESTION" etc.
    )
    return [embedding["value"] for embedding in embeddings["embedding"]]


if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_API_KEY environment variable is set.
    # messages = [
    #     "Database connection error.",
    #     "Failed to connect to the SQL server.",
    #     "User login successful.",
    #     "Application started successfully."
    # ]
    # message_embeddings = embed_log_messages(messages)
    # for i, embedding in enumerate(message_embeddings):
    #     print(f"Embedding for '{messages[i]}': {embedding[:5]}...") # Print first 5 values for brevity
    pass
