import os
import openai
from typing import List
from storage_models import EmbedTextRequest, EmbedTextResponse

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def embed_asset_text(request: EmbedTextRequest) -> EmbedTextResponse:
    if not OPENAI_API_KEY:
        return EmbedTextResponse(success=False, error_message="OPENAI_API_KEY environment variable not set")

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    try:
        # Using text-embedding-ada-002 for embeddings
        response = client.embeddings.create(
            input=[request.text],
            model="text-embedding-ada-002"
        )
        embedding = response.data[0].embedding
        return EmbedTextResponse(success=True, embedding=embedding)
    except Exception as e:
        return EmbedTextResponse(success=False, error_message=str(e))
