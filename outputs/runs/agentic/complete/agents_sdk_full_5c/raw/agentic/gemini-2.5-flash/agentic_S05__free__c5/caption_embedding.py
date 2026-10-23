import asyncio
import os
from typing import List, Tuple

import google.generativeai as genai

# Configure Google Generative AI API key
# export GOOGLE_API_KEY="your-google-api-key"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class CaptionEmbedder:
    def __init__(self, api_key: str, model_name: str = "text-embedding-004"):
        if not api_key:
            raise ValueError("Google API Key must be provided for embeddings.")
        genai.configure(api_key=api_key)
        self.model_name = model_name
        print(f"Initialized CaptionEmbedder with model: {self.model_name}")

    async def embed_text(self, text: str) -> List[float]:
        """Generates an embedding for a given text using Google's Generative AI."""
        if not text.strip():
            return []
        
        try:
            # The `embed_content` method is synchronous, so we run it in a thread pool
            response = await asyncio.to_thread(
                genai.embed_content,
                model=self.model_name,
                content=text,
                task_type="RETRIEVAL_DOCUMENT" # or "SEMANTIC_SIMILARITY", "AQA_QUESTION", etc.
            )
            if response and response['embedding']:
                return response['embedding']
            return []
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []

    async def process_captions_for_embedding(self, caption_stream: AsyncIterable[Tuple[str, bool]]):
        """Processes a stream of live captions and yields text and their embeddings."""
        print("\n--- Caption Embedding Pipeline ---")
        async for transcript, is_final in caption_stream:
            if is_final and transcript.strip():
                embedding = await self.embed_text(transcript)
                if embedding:
                    print(f"Embedded Final Caption (dim {len(embedding)}): '{transcript}'")
                    # In a real scenario, you'd store this embedding in a vector database
                    # along with the transcript for semantic search.
                    yield transcript, embedding, is_final
                else:
                    print(f"Failed to embed final caption: '{transcript}'")
                    yield transcript, [], is_final
            elif transcript.strip():
                print(f"Partial Caption (not embedding): '{transcript}'")
                yield transcript, [], is_final

async def mock_caption_stream_for_embedding():
    """A mock async generator for caption chunks."""
    yield "The team discussed the Q1 financial results and strong growth.", True
    await asyncio.sleep(1)
    yield "We need to allocate resources for the new product launch.", True
    await asyncio.sleep(1)
    yield "Marketing strategy involves social media campaigns.", True
    await asyncio.sleep(1)
    yield "Competitor analysis showed a gap in our current offerings.", True

async def main():
    api_key = GOOGLE_API_KEY
    if not api_key:
        print("Warning: GOOGLE_API_KEY environment variable not set. Embeddings will not work.")
        print("Please set the GOOGLE_API_KEY environment variable.")
        return

    embedder = CaptionEmbedder(api_key=api_key)
    async for transcript, embedding, is_final in embedder.process_captions_for_embedding(mock_caption_stream_for_embedding()):
        # Example of how you might use the embedding for similarity search (conceptual)
        # if embedding:
        #     print(f"  First 5 dimensions of embedding: {embedding[:5]}...")
        pass # The pipeline function already prints.

if __name__ == "__main__":
    asyncio.run(main())
