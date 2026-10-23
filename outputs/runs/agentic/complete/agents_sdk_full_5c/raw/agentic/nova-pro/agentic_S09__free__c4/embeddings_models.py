class EmbeddingRequest:
    def __init__(self, text):
        self.text = text

class EmbeddingResponse:
    def __init__(self, embedding):
        self.embedding = embedding