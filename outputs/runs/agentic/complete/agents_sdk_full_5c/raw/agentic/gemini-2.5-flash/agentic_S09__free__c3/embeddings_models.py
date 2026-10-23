from typing import List, Dict, Any

# Define common embedding model names or other constants
OPENAI_DEFAULT_EMBEDDING_MODEL = "text-embedding-ada-002"

# Example of a simple Pydantic-like structure if more complex data models were needed
# For this challenge, we'll keep it simple as the OpenAI SDK returns structured objects.

class EmbeddingResult:
    """A simple structure to represent an embedding result.
    (This is more for conceptual clarity, as the OpenAI SDK returns its own objects).
    """
    def __init__(self, embedding: List[float], text_index: int = 0, model: str = OPENAI_DEFAULT_EMBEDDING_MODEL):
        self.embedding = embedding
        self.text_index = text_index
        self.model = model

    def to_dict(self) -> Dict[str, Any]:
        return {
            "embedding": self.embedding,
            "text_index": self.text_index,
            "model": self.model,
        }
