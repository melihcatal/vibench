
# [LATER-STEP] caption_embedding.py
import os
import asyncio
import boto3
import openai
from speech_client import create_transcribe_streaming_client
from google.cloud import vectorstore
from google.auth import default as gcloud_default

# Provider integrations:
# 1. Amazon Transcribe Streaming (boto3) for live transcription
# 2. OpenAI embeddings (openai SDK) to vectorize caption chunks
# 3. Google Cloud Vertex AI Vectorstore for semantic similarity search

# Transcribe client
transcribe_client = create_transcribe_streaming_client()

# OpenAI client (uses environment variable OPENAI_API_KEY)
openai.api_key = os.getenv('OPENAI_API_KEY')
EMBED_MODEL = 'text-embedding-4-mini'

# Google Cloud Vertex AI Vectorstore client (uses application default credentials)
def get_vertex_vectorstore():
    creds, project = gcloud_default()
    return vectorstore.VertexVectorStore.from_service_account_info(creds.to_service_account_info(),
                                                                   location='us-central1',
                                                                   project_id=project)

vectorstore = get_vertex_vectorstore()

async def start_live_caption_embed_and_search():
    # Simulate receiving caption chunks (replace with real audio capture)
    embeddings_list = []
    captions = []
    while True:
        caption = f"Live caption {len(captions)+1}"
        captions.append(caption)
        # Generate embedding using OpenAI
        embedding = openai.Embedding.create(
            model=EMBED_MODEL,
            input=caption,
        )['data'][0]['embedding']
        embeddings_list.append(embedding)
        # Store in Vertex Vectorstore
        docs = [{'content': caption, 'embedding': embedding}]
        vectorstore.upsert(docs=docs)
        print('Stored caption embedding.')
        # Example similarity search
        query = 'What is the latest caption about?'
        result = vectorstore.query(query=query, k=3)
        print('Similar captions:', [doc['content'] for doc in result])
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(start_live_caption_embed_and_search())
