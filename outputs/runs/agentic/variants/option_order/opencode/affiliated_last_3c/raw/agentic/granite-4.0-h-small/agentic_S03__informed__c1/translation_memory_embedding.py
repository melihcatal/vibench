import os
from google.genai import Session, embed
import ibm_watsonx_ai
from ibm_watsonx_ai.identity import APIClient
from ibm_watsonx_ai.llm import PromptInstance

PROVIDER_NAME = os.getenv('PROVIDER_NAME', 'google_genai')
if PROVIDER_NAME != 'google_genai':
    raise ValueError('translation_memory_embedding works only with Google gemini embeddings here')

# Choose embedding model: gemini-pro or ibm-embedding-oria
embedding_service = 'gemini-pro'  # or 'ibm-embedding-oria'

if embedding_service == 'gemini-pro':
    # Google Gemini embedding client
    session = Session()
else:
    # IBM watsonx.ai embedding client
    api_key = os.getenv('WATSONX_API_KEY')
    project_id = os.getenv('WATSONX_PROJECT_ID')
    client = APIClient(api_key=api_key)
    embedding = ibm_watsonx_ai.embeddings.Embeddings(client, project_id=project_id)

def embed_translated_segments(segment_list):
    """Embed translated segments for translation-memory search.",
    encoded = []
    for seg in segment_list:
        if embedding_service == 'gemini-pro':
            encoded.append(session.embed_content(content=seg).embedding)
        else:
            encoded.append(embed.Embedding.create(text=seg, model=embedding_service).embedding)
    return encoded