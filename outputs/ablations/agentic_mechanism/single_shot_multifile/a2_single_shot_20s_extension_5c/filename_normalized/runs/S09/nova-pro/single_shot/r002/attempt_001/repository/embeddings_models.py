class EmbeddingRequest:
    def __init__(self, text):
        self.text = text

class BatchEmbeddingRequest:
    def __init__(self, texts):
        self.texts = texts

class EmbeddingResponse:
    def __init__(self, embedding):
        self.embedding = embedding

class BatchEmbeddingResponse:
    def __init__(self, embeddings):
        self.embeddings = embeddings