class EmbeddingsInput:

    def __init__(self, text):
        self.text = text

    def to_json(self):
        return {"inputText": self.text}


class EmbeddingsOutput:

    def __init__(self, embedding):
        self.embedding = embedding

    @classmethod
    def from_json(cls, json_data):
        return cls(json_data["embedding"])
