import asyncio
import os
from typing import AsyncIterable

import google.auth
from google.cloud import generativeai as genai
from google.cloud import storage

# Initialize Gemini model for embeddings (environment variable)
GENAI_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GENAI_API_KEY)
EMBED_MODEL = "gemini-1.5-flash-lightning"

# Optional: store embeddings in Cloud Storage (configure bucket name via env)
BLOB_BUCKET = os.getenv("EMBEDDING_BUCKET", "meeting-embeddings")
BLOB_NAME = "captions/embedding_{index}.json"
storage_client = storage.Client()


async def embed_captions(
    captions: AsyncIterable[str], *, index: int = 0
) -> AsyncIterable[Dict[str, Any]]:
    """Creates embeddings for each caption chunk using Gemini and yields a dict with metadata."""
    embed = genai.GenerativeModel(EMBED_MODEL)
    for caption in captions:
        resp = embed.embed_content(caption)
        embedding = resp.embeddings[0].embedding  # list of floats
        meta = {"caption": caption, "embedding": embedding, "index": index}
        # Optionally upload to Cloud Storage for persistence
        blob = storage_client.bucket(BLOB_BUCKET).blob(BLOB_NAME.format(index=index))
        blob.upload_from_string(json.dumps(meta))
        yield meta
        index += 1


# Example usage with a caption generator (e.g., from live_caption_translate)
# async for meta in embed_captions(translate_live_captions(stream_microphone_events)):
#     print("Embedded:", meta)
