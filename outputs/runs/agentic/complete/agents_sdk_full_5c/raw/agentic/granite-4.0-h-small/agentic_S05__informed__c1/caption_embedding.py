import asyncio
import json
import os
from ibm_watsonx_ai.embeddings import EmbeddingsClient
from ibm_watsonx_ai.auth import IAMTokenManager
# Optional: Azure OpenAI embeddings, OpenAI embeddings, etc. demonstrated via import paths

# IBM watsonx.ai embedding model (Slate) reference provider
WATSONX_APIKEY = os.getenv('WATSONX_API_KEY')
WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')
token_manager = IAMTokenManager(apikey=WATSONX_APIKEY)
client = EmbeddingsClient(token_manager=token_manager)
EMBED_MODEL = 'ibm/granite-embed-3b'  # model family identifier

async def embed_caption_chunks(caption_chunks):
    """Embed each caption chunk using watsonx.ai embeddings and return a list of vectors."""
    vectors = []
    async for chunk in caption_chunks:
        response = client.create_embeddings(
            input=chunk,
            model_id=EMBED_MODEL,
        )
        # response contains list of embeddings per input
        embeds = response.get('result', {}).get('embeddings', [])
        if embeds:
            vectors.append(embeds[0]['embedding'])  # each chunk returns one vector
    print('Captions embedded, total vectors:', len(vectors))
    return vectors

# Example placeholder asynchronous caption source
# async def caption_source():
#     while True:
#         chunk = await get_next_caption()
#         yield chunk

# asyncio.run(embed_caption_chunks(caption_source()))
