import os
import asyncio
import cohere
from typing import AsyncGenerator, Dict, Any, List

# Cohere client setup
# Ensure COHERE_API_KEY environment variable is set.

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

async def embed_caption_chunks(caption_generator: AsyncGenerator[str, None], model_name: str = "embed-english-v3.0") -> AsyncGenerator[Dict[str, Any], None]:
    if not COHERE_API_KEY:
        print("WARNING: Cohere API key is not set. Please set COHERE_API_KEY environment variable.")
        # In a real application, you might raise an error or exit.
        # For this example, we will proceed but it will fail if the key is truly missing.
        return

    client = cohere.Client(api_key=COHERE_API_KEY)

    print(f"Starting caption embedding using Cohere Embed model: {model_name}...")
    print("Please ensure your COHERE_API_KEY is correctly set.")

    async for caption_chunk in caption_generator:
        if not caption_chunk.strip():
            continue

        try:
            # Cohere Embed API call
            # For chunks, we embed each chunk. For more sophisticated search, 
            # you might concatenate chunks or use a sliding window.
            response = client.embed(
                texts=[caption_chunk],
                model=model_name,
                input_type="search_query" # or "classification", "clustering", "reranker", etc.
            )
            embedding = response.embeddings[0] if response.embeddings else []
            
            yield {
                "caption_chunk": caption_chunk,
                "embedding": embedding
            }

        except Exception as e:
            print(f"Error embedding caption chunk '{caption_chunk}': {e}")
            yield {"error": str(e), "caption_chunk": caption_chunk}

if __name__ == "__main__":
    async def dummy_caption_stream():
        chunks = [
            "The quick brown fox jumps over the lazy dog.",
            "Artificial intelligence is transforming industries globally.",
            "Meeting discussing Q3 financial results and marketing ROI.",
            "I need to review the budget for next quarter."
        ]
        for chunk in chunks:
            await asyncio.sleep(1)
            yield chunk

    async def main():
        print("Running caption embedding example with Cohere Embed.")
        async for result in embed_caption_chunks(dummy_caption_stream()):
            if "embedding" in result:
                print(f"Caption: '{result['caption_chunk']}'")
                print(f"Embedding (first 5 values): {result['embedding'][:5]}...")
                print(f"Embedding dimension: {len(result['embedding'])}")
                print("---------------------")
            elif "error" in result:
                print(f"Error embedding caption '{result['caption_chunk']}': {result['error']}")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Embedding stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")
