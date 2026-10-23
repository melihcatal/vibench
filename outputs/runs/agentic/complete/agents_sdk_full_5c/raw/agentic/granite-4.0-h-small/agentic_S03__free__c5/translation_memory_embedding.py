import os
import openai
import json
from typing import List

TRANSLATION_MEMORY_EMBED_MODEL = os.getenv('TRANSLATION_MEMORY_EMBED_MODEL', 'text-embedding-ada-002')

def embed_text(text: str) -> List[float]:
    """Embed a segment using OpenAI embedding endpoint."""
    response = openai.Embedding.create(model=TRANSLATION_MEMORY_EMBED_MODEL, input=text)
    return response['data'][0]['embedding']

# Simple demo: embed a list and write to file for later search
if __name__ == '__main__':
    segments = ['Hello world', 'Bonjour le monde', 'Hallo Welt']
    embeddings = [embed_text(s) for s in segments]
    with open('translation_memory_embeddings.pkl', 'wb') as f:
        import pickle
        pickle.dump(embeddings, f)
    print('Embedded segments and stored in translation_memory_embeddings.pkl')
