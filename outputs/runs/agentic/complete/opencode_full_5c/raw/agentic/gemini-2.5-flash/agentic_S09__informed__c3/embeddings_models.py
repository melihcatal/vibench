from dataclasses import dataclass
from typing import List

# Define a constant for the embedding model name
EMBEDDING_MODEL_NAME = "models/embedding-001"


@dataclass
class EmbedTextRequest:
    """
    Represents a request to embed a single text string.
    """

    text: str
    model: str = EMBEDDING_MODEL_NAME
    task_type: str = "RETRIEVAL_DOCUMENT"


@dataclass
class EmbedBatchRequest:
    """
    Represents a request to embed a batch of text strings.
    """

    texts: List[str]
    model: str = EMBEDDING_MODEL_NAME
    task_type: str = "RETRIEVAL_DOCUMENT"


@dataclass
class EmbeddingResponse:
    """
    Represents the response containing embedding vectors.
    """

    embedding: List[float]


@dataclass
class BatchEmbeddingResponse:
    """
    Represents the response containing multiple embedding vectors for a batch request.
    """

    embeddings: List[EmbeddingResponse]
