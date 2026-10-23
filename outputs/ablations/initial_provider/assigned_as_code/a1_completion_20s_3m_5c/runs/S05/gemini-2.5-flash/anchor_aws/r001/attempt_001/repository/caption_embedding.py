import os
from typing import AsyncIterable, List

import google.generativeai as genai

from speech_models import TranscriptSegment

async def caption_embedding(transcript_segments: AsyncIterable[TranscriptSegment]):
    # Configure the Gemini API client
    # Ensure GOOGLE_API_KEY is set in your environment variables
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    async for segment in transcript_segments:
        if segment.text:
            try:
                response = genai.embed_content(
                    model="models/text-embedding-004", # Using a text embedding model
                    content=segment.text,
                    task_type="RETRIEVAL_DOCUMENT",
                )
                embedding = response['embedding']
                print(f"Transcript: '{segment.text}' | Embedding Length: {len(embedding)}")
                yield {"text": segment.text, "embedding": embedding, "is_final": segment.is_final}
            except Exception as e:
                print(f"Error generating embedding for '{segment.text}': {e}")
                yield {"text": segment.text, "embedding": None, "is_final": segment.is_final, "error": str(e)}
