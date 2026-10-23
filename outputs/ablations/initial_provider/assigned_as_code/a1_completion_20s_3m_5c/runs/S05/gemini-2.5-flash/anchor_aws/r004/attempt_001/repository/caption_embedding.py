import os
import openai

def caption_embedding(caption_chunks):
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    full_caption = " ".join(caption_chunks)

    response = openai.embeddings.create(
        input=[full_caption],
        model="text-embedding-ada-002"  # Using a concrete model identifier
    )
    return response.data[0].embedding
