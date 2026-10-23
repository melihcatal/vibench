import os
from openai import OpenAI
from speech_models import EmbeddingRequest
from typing import List

def get_script_embedding(request: EmbeddingRequest) -> List[float]:
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")

    client = OpenAI(api_key=openai_api_key)

    # Using a common embedding model. This can be made configurable if needed.
    model_name = "text-embedding-ada-002"

    response = client.embeddings.create(input=[request.text], model=model_name)

    if response.data:
        return response.data[0].embedding
    else:
        raise Exception("Embedding failed: No data returned.")
