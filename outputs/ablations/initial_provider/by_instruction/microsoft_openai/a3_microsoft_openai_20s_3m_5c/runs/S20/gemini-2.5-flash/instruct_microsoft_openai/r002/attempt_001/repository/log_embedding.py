from observability_client import OpenAIClient
from observability_models import EmbeddedMessage
from typing import List

def embed_log_messages(log_messages: List[str]) -> List[EmbeddedMessage]:
    openai_client = OpenAIClient()
    embedded_results: List[EmbeddedMessage] = []

    for message in log_messages:
        embedding_vector = openai_client.get_embedding(message)
        embedded_results.append(EmbeddedMessage(
            original_text=message,
            embedding=embedding_vector
        ))
    return embedded_results

if __name__ == "__main__":
    # Example log messages
    sample_log_messages = [
        "Failed to connect to the database. Check network connectivity and credentials.",
        "Database connection refused by host. Is the database service running?",
        "User 'john.doe' successfully logged in from IP 192.168.1.10.",
        "Authentication failure: Invalid password for user 'jane.doe'."
    ]

    print("Generating embeddings for log messages...")
    embedded_logs = embed_log_messages(sample_log_messages)

    for i, res in enumerate(embedded_logs):
        print(f"\n--- Log Message {i+1} ---")
        print(f"Original: {res.original_text}")
        print(f"Embedding (first 5 dimensions): {res.embedding[:5]}...")
        print(f"Embedding Length: {len(res.embedding)}")
