import google.generativeai as genai
import os
from speech_models import TranscriptResult

class CaptionEmbedder:
    def __init__(self, model_name: str = "embedding-001"):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Please set the GEMINI_API_KEY environment variable.")
        genai.configure(api_key=api_key)
        self.model = model_name

    async def embed_caption_chunk(self, caption_chunk: str) -> list[float]:
        if not caption_chunk.strip():
            return []
        
        try:
            response = await genai.embed_content_async(model=self.model, content=caption_chunk)
            embedding = response['embedding']
            print(f"Embedding for \" {caption_chunk[:30]}... \" generated.")
            return embedding
        except Exception as e:
            print(f"Error generating embedding for chunk: {e}")
            return []

if __name__ == "__main__":
    # Example usage
    embedder = CaptionEmbedder()
    sample_caption_chunk = """
    We need to discuss the new marketing strategy for the upcoming quarter. 
    The previous quarter's results were not as expected, primarily due to 
    ineffective social media campaigns. Let's brainstorm some fresh ideas.
    """
    
    async def run_embedding_example():
        embedding = await embedder.embed_caption_chunk(sample_caption_chunk)
        print(f"Embedding (first 5 elements): {embedding[:5]}...")

    import asyncio
    asyncio.run(run_embedding_example())
