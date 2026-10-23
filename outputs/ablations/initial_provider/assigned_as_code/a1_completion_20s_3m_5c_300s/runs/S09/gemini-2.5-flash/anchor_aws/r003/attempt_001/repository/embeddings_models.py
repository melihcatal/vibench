class EmbeddingsRequest:
    def __init__(self, texts):
        self.texts = texts

    def to_bedrock_batch_input(self):
        # For models like Titan Text Embeddings, each text is a separate call
        # This method prepares a list of individual inputs.
        return [{"inputText": text} for text in self.texts]


class EmbeddingsResponse:
    def __init__(self, bedrock_response_data):
        self.embeddings = [item["embedding"] for item in bedrock_response_data]


def normalize_embedding(embedding):
    # Basic normalization (e.g., to unit vector) if needed. Bedrock embeddings are often already normalized.
    # For simplicity, we return as is here.
    return embedding
