from openai import OpenAI
from speech_models import EmbeddingRequest
import os

def get_transcript_embeddings(request: EmbeddingRequest) -> list[list[float]]:
    # OpenAI Embeddings API
    # Set OPENAI_API_KEY environment variable
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    response = client.embeddings.create(
        input=request.text_segments,
        model="text-embedding-ada-002" # Using a common embedding model
    )
    
    embeddings = []
    for data in response.data:
        embeddings.append(data.embedding)
        
    return embeddings
