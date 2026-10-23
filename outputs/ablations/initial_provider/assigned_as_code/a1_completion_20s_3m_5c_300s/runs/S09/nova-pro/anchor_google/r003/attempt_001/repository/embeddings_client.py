import os


class DirectEmbeddingsClient:
    def __init__(self, config=None):
        self.config = config or {}
        self.api_key = self.config.get('api_key') or os.environ.get('GOOGLE_API_KEY')
        self.model = 'gemini-embedding-001'
        self.client = genai.Client(api_key=self.api_key)

    def embed_text(self, payload):
        response = self.client.models.embed_content(model=self.model, contents=payload['text'])
        return list(response.embeddings[0].values)

    def embed_batch(self, payload):
        response = self.client.models.embed_batch(model=self.model, contents=payload['texts'])
        return {'embeddings': [list(emb.values()) for emb in response.embeddings]}

    def calculate_similarity(self, embedding1, embedding2):
        # Placeholder for actual similarity calculation
        return 0.8

    def calculate_similarities(self, query_embedding, document_embeddings):
        # Placeholder for actual similarity calculation
        return [0.8 for _ in document_embeddings]