import os
import cohere

def embed_caption_chunks(caption_generator):
    api_key = os.getenv('COHERE_API_KEY')
    if not api_key:
        raise ValueError('COHERE_API_KEY environment variable is required.')
    co = cohere.Client(api_key)
    for caption in caption_generator:
        if caption.strip():
            embedding = co.embed(
                texts=[caption],
                model='embed-english-v3.0',
                input_type='search_query'
            ).embeddings[0]
            yield embedding
        else:
            yield [0.0] * 1024  # Dummy embedding