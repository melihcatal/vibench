# Embed extracted document sections for semantic retrieval using OpenAI embeddings
import os
import openai

class OpenAIEncoder:
    """Wrapper around OpenAI's embedding model."""
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        if not openai.api_key:
            raise RuntimeError('Set OPENAI_API_KEY environment variable')

    def embed_section(self, text: str) -> list:
        """Return a list of floats representing the embedding of `text`."""
        resp = openai.Embedding.create(model='text-embedding-ada-002', input=text)
        return resp['data'][0]['embedding']

    @classmethod
    def from_response(cls, resp: str) -> 'OpenAIEncoder':
        return cls()
