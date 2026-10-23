import os
from openai import OpenAI

def embed_outputs(outputs: list[str]) -> list[list[float]]:
    """
    Embeds model outputs using OpenAI's text-embedding-ada-002 model.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=outputs,
        model="text-embedding-ada-002"
    )
    return [d.embedding for d in response.data]

if __name__ == "__main__":
    # Example usage
    model_outputs = [
        "This is the first model output.",
        "Here is another output from the model.",
        "A third example of model output for embedding."
    ]
    embeddings = embed_outputs(model_outputs)
    for i, embedding in enumerate(embeddings):
        print(f"Embedding for output {i+1}: {embedding[:5]}...") # Print first 5 dimensions
