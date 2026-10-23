import asyncio
from typing import List
import vertexai
from vertexai.language_models import TextEmbeddingModel
from speech_models import SpeechRecognitionResult

# Google Cloud Vertex AI Embeddings for Text uses the `vertexai` SDK
# and `TextEmbeddingModel` for its operations.
# The model identifier for text embedding is `textembedding-gecko@001` or similar.


def initialize_vertex_ai(project: str, location: str):
    vertexai.init(project=project, location=location)


async def embed_text_chunk(text_chunk: str) -> List[float]:
    """
    Embeds a single text chunk using Google Cloud Vertex AI Embeddings for Text.

    Args:
        text_chunk: The text chunk to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    # Ensure Vertex AI is initialized. Replace with your project and region.
    try:
        if not vertexai.initializer._is_initialized:
            initialize_vertex_ai(project="your-gcp-project-id", location="us-central1")
    except Exception:
        print(
            "Warning: Vertex AI not explicitly initialized with project/location. "
            "Ensure `gcloud auth application-default login` has been run or "
            "project/location are set programmatically."
        )

    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    embeddings = model.get_embeddings([text_chunk])

    if embeddings:
        return embeddings[0].values
    return []


async def caption_embedding_stream(caption_stream_generator):
    """
    Asynchronously embeds live caption chunks for semantic search.

    Args:
        caption_stream_generator: An async generator yielding SpeechRecognitionResult objects.

    Yields:
        Tuple[str, List[float]]: Original caption and its embedding vector.
    """
    print("Starting caption embedding...")
    async for caption_result in caption_stream_generator:
        if caption_result.is_final and caption_result.transcript.strip():
            embedding = await embed_text_chunk(caption_result.transcript)
            print(
                f'Caption: "{caption_result.transcript}" -> Embedding vector length: {len(embedding)}'
            )
            yield caption_result.transcript, embedding
