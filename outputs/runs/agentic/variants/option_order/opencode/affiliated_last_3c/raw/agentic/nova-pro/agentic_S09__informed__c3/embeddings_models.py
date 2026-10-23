class EmbeddingRequest:
    def __init__(self, input, model="text-embedding-ada-002"):
        self.input = input
        self.model = model


class EmbeddingResponse:
    def __init__(self, embedding):
        self.embedding = embedding


def normalize_response(response):
    return [item["embedding"] for item in response["data"]]
