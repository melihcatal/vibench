from typing import List, Dict, Any

# Define local request, response, and normalization helpers for Hosted LLM Inference and Model-Family Selection


class GeminiPromptRequest:
    def __init__(self, text: str):
        self.text = text


class GeminiResponse:
    def __init__(self, text: str):
        self.text = text

    @classmethod
    def from_gemini_content_response(cls, response: Any):
        # A simplified normalization for demonstration
        return cls(text=response.text)


class GeminiEmbeddingRequest:
    def __init__(self, text: List[str]):
        self.text = text


class GeminiEmbeddingResponse:
    def __init__(self, embedding: List[float]):
        self.embedding = embedding

    @classmethod
    def from_gemini_embedding_response(cls, response: Any):
        # A simplified normalization for demonstration
        return cls(
            embedding=response["embedding"][0]
        )  # Assuming single text input for simplicity
