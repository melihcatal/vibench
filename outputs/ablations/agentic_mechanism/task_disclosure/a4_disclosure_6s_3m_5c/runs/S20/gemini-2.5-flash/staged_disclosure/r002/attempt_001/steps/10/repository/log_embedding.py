import openai
import os

def get_embedding(text: str, model: str = "text-embedding-ada-002") -> list[float]:
    """
    Generates an embedding for a given text using OpenAI's API.
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

def embed_log_messages(log_messages: list[str], model: str = "text-embedding-ada-002") -> list[list[float]]:
    """
    Generates embeddings for a list of log messages using OpenAI's API.
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(input=log_messages, model=model)
    return [data.embedding for data in response.data]

if __name__ == "__main__":
    # Example Usage:
    # Set your OpenAI API key as an environment variable or replace os.environ.get("OPENAI_API_KEY") with your actual key
    # For example: export OPENAI_API_KEY="your_openai_api_key_here"

    log_message = "User login failed due to incorrect password."
    embedding = get_embedding(log_message)
    print(f"Embedding for single message (first 5 elements): {embedding[:5]}...")

    log_messages_list = [
        "Database connection error: Could not connect to host.",
        "Application started successfully on port 8080.",
        "User login failed due to incorrect password.",
        "File not found: /var/log/app.log"
    ]
    embeddings_list = embed_log_messages(log_messages_list)
    print(f"Embeddings for list of messages (first 5 elements of first embedding): {embeddings_list[0][:5]}...")
