import asyncio
from typing import List
import cohere
from speech_client import SpeechClient
from speech_models import TranscriptResult

async def embed_caption_chunk(text: str) -> List[float]:
    client = SpeechClient().get_cohere_client()

    if not client.api_key:
        print("Cohere API key not configured. Please set COHERE_API_KEY environment variable.")
        return []

    # Cohere model identification signal: 'embed' method and 'model' parameter
    try:
        # The model "embed-english-v3.0" is a common choice for English embeddings
        # Other models like "embed-multilingual-v3.0" can be used for multiple languages
        response = client.embed(
            texts=[text],
            model="embed-english-v3.0", # Cohere embedding model
            input_type="search_document", # Specify input_type for optimal performance
        )
        embeddings = response.embeddings[0] # Get the embedding for the first (and only) text
        return embeddings
    except Exception as e:
        print(f"Error generating embedding with Cohere: {e}")
        return []

async def simulated_caption_stream(num_captions: int = 3):
    captions = [
        "The project deadline is approaching rapidly and we need to accelerate.",
        "Let's review the outstanding tasks and assign owners for each item.",
        "The financial report indicates a strong performance in the last quarter."
    ]
    for i in range(min(num_captions, len(captions))):
        yield TranscriptResult(transcript=captions[i], is_partial=False, language_code="en-US")
        await asyncio.sleep(0.5)

if __name__ == "__main__":
    async def main():
        print("Demonstrating caption embedding using Cohere.")
        async for caption_result in simulated_caption_stream():
            print(f"Embedding caption: \"{caption_result.transcript}\" ")
            embedding = await embed_caption_chunk(caption_result.transcript)
            print(f"Generated Embedding (first 5 values): {embedding[:5]}... (total {len(embedding)} values)\n")
    asyncio.run(main())
