import asyncio
import aiohttp
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import language_v1 as language
from speech_models import build_config

EMBEDDING_MODEL = "textembedding-gecko"


def get_language_client():
    """
    Helper to create a LanguageServiceClient for embedding generation.
    Uses GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    return language.LanguageServiceClient()  # concrete GCP provider


def embed(text: str) -> str:
    """
    Calls the Vertex AI embedding endpoint.
    Returns a compact base64 vector representation as a placeholder.
    """
    client = get_language_client()
    response = client.get_document_embedding(
        document=language.Document(content=text, type=language.Document.Type.PLAIN_TEXT)
    )
    vector = response.embedding.embedding_data
    # Convert vector to string representation (demo)
    return str(vector)


async def caption_embedding(audio_iterable):
    client = speech.SpeechClient()  # concrete GCP provider
    config = build_config(language_code="en-US")
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=False
    )
    requests = [speech.StreamingRecognizeRequest(streaming_config=streaming_config)]
    async for chunk in audio_iterable:
        requests.append(speech.StreamingRecognizeRequest(audio_content=chunk))
    payload = {"config": config, "requests": requests}
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://speech.googleapis.com/v1p1beta1/speech:recognizeStreaming",
            json=payload,
        ) as resp:
            results = await resp.json()
            all_captions = []
            for result in results.get("results", []):
                alt = result.get("alternatives", [{}])[0]
                if not alt.get("is_final"):
                    continue
                caption = alt["transcript"]
                all_captions.append(caption)
            # Generate embeddings for each caption
            for caption in all_captions:
                vec = embed(caption)
                print(f"Embedding for '{caption}': {vec[:30]}...")
