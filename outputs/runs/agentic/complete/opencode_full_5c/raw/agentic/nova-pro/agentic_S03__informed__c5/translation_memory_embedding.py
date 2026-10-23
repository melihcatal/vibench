import os
import cohere


def translation_memory_embedding(text):
    cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = cohere_client.embed(texts=[text])
    return response.embeddings[0]


if __name__ == "__main__":
    print(translation_memory_embedding("Hello, world!"))
