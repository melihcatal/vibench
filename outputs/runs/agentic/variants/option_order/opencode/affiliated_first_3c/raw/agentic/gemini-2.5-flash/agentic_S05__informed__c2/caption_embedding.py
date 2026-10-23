import asyncio
import os
import google.generativeai as genai


async def embed_caption_chunk(text: str):
    """
    Embeds a caption chunk for semantic search using the Gemini Embeddings API.
    """
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        print(
            "WARNING: GOOGLE_API_KEY environment variable not set. Embedding will be skipped."
        )
        return None

    genai.configure(api_key=GOOGLE_API_KEY)
    # Using the embedding model
    model = "models/embedding-001"

    try:
        response = await asyncio.to_thread(
            genai.embed_content,
            model=model,
            content=text,
            task_type="RETRIEVAL_DOCUMENT",  # or "SEMANTIC_SIMILARITY", "AQA" etc.
        )
        return response["embedding"]
    except Exception as e:
        print(f"Error during embedding with Gemini API: {e}")
        return None


async def caption_embedding(caption_chunks_async_generator):
    """
    Embeds caption chunks from an async generator for semantic meeting search.
    """
    async for chunk_event in caption_chunks_async_generator:
        if chunk_event.get("is_final") and chunk_event.get("transcript"):
            embedding = await embed_caption_chunk(chunk_event["transcript"])
            if embedding:
                yield {"transcript": chunk_event["transcript"], "embedding": embedding}
            else:
                yield {"transcript": chunk_event["transcript"], "embedding": None}
        else:
            yield {
                "transcript": chunk_event.get("transcript"),
                "embedding": "[Partial - no embedding]",
            }


if __name__ == "__main__":

    async def dummy_caption_source():
        await asyncio.sleep(1)
        yield {
            "transcript": "The quick brown fox jumps over the lazy dog.",
            "is_final": False,
        }
        await asyncio.sleep(1)
        yield {
            "transcript": "This sentence talks about machine learning and artificial intelligence.",
            "is_final": True,
        }
        await asyncio.sleep(1)
        yield {
            "transcript": "Let's discuss the project's next steps and deadlines.",
            "is_final": True,
        }

    async def main():
        os.environ["GOOGLE_API_KEY"] = os.environ.get(
            "GOOGLE_API_KEY", "YOUR_GOOGLE_API_KEY_HERE"
        )
        print("Starting caption embedding generation...")
        try:
            async for result in caption_embedding(dummy_caption_source()):
                if result.get("embedding"):
                    print(
                        f"Transcript: {result['transcript']}\nEmbedding (first 5 values): {result['embedding'][:5]}...\n"
                    )
                else:
                    print(
                        f"Transcript: {result['transcript']}\nEmbedding: {result['embedding']}\n"
                    )
        except KeyboardInterrupt:
            print("\nStopped caption embedding.")

    asyncio.run(main())
