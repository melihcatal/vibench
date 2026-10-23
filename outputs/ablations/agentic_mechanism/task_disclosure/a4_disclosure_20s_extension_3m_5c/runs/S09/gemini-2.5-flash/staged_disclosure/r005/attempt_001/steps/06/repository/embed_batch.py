import openai

def generate_embeddings_batch(texts: list[str], api_key: str) -> list[list[float]]:
    """
    Generates embeddings for a batch of texts using OpenAI's text-embedding-ada-002 model.

    Args:
        texts: A list of strings to generate embeddings for.
        api_key: Your OpenAI API key.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    client = openai.OpenAI(api_key=api_key)
    response = client.embeddings.create(
        input=texts,
        model="text-embedding-ada-002"
    )
    return [item.embedding for item in response.data]

if __name__ == "__main__":
    # Example usage:
    # Replace "YOUR_OPENAI_API_KEY" with your actual OpenAI API key
    # It is recommended to load the API key from environment variables for production use
    # For example: api_key = os.environ.get("OPENAI_API_KEY")
    openai_api_key = "YOUR_OPENAI_API_KEY" 

    if openai_api_key == "YOUR_OPENAI_API_KEY":
        print("Please replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key.")
    else:
        sample_texts = [
            "This is the first sentence.",
            "This is the second sentence, it is about something else.",
            "And this is the third one.",
        ]
        embeddings = generate_embeddings_batch(sample_texts, openai_api_key)
        for i, embedding in enumerate(embeddings):
            print(f"Embedding for text {i+1}: {embedding[:5]}...") # Print first 5 dimensions
        print(f"Number of embeddings generated: {len(embeddings)}")
        if embeddings:
            print(f"Dimension of each embedding: {len(embeddings[0])}")
