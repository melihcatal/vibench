# [LATER-STEP] caption_embedding.py
# Embed caption chunks for semantic meeting search using IBM Slat Embeddings (watsonx.ai embeddings)
import os
from ibm_watsonx_ai import Client
from ibm_watsonx_ai.embed.embed_client import EmbedClient
from ibm_watsonx_ai.embed.models import TextEmbeddingRequest

# Provider configuration
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Create embed client
embed_client = EmbedClient(project_id=WATSONX_PROJECT_ID, api_key=WATSONX_API_KEY)


async def embed_text(text):
    request = TextEmbeddingRequest(content=[text])
    # For simplicity we use the default 'all-MiniLM-L6-v2' model
    response = await embed_client.embed_text(request)
    # response.embeddings = list of embedding vectors per input
    return response.embeddings[0]


if __name__ == "__main__":
    # Placeholder for caption chunk
    embedding = embed_text(
        "Project kickoff meeting started. Agenda includes roadmap discussion."
    )
    print(embedding)
