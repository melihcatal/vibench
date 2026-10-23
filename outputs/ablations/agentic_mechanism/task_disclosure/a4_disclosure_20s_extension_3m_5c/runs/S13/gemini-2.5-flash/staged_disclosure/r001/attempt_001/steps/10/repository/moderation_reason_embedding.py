import os
import openai

def embed_moderation_reason(reason: str) -> list[float]:
    """
    Embeds a moderation reason using OpenAI's embedding model.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    # Using a specific OpenAI embedding model
    model_id = "text-embedding-ada-002" 

    try:
        response = openai.embeddings.create(
            input=reason,
            model=model_id
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error embedding reason: {e}")
        return []

if __name__ == "__main__":
    test_reason = "This content violates our community guidelines due to hate speech."
    embedding = embed_moderation_reason(test_reason)
    if embedding:
        print(f"Embedding successful. Length: {len(embedding)}")
        # print(f"First 5 dimensions of embedding: {embedding[:5]}")
    else:
        print("Embedding failed.")
