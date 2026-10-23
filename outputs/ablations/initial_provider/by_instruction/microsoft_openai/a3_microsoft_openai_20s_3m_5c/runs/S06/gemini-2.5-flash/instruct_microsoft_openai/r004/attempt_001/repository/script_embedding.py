from speech_client import OpenAIClient
from speech_models import EmbeddingInput, EmbeddingOutput

def script_embedding(input: EmbeddingInput) -> EmbeddingOutput:
    client = OpenAIClient()
    response = client.embeddings.create(
        input=input.text,
        model="text-embedding-ada-002", # OpenAI embedding model
    )
    embedding = response.data[0].embedding
    return EmbeddingOutput(embedding=embedding)
