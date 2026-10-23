from typing import List
import os
import cohere

def moderation_reason_embedding(rationale: str) -> List[float]:
    api_key = os.getenv(&quot;COHERE_API_KEY&quot;)
    co = cohere.Client(api_key)
    response = co.embed(
        model=&quot;embed-english-v3.0&quot;,
        texts=[rationale],
        input_type=&quot;search_query&quot;
    )
    return response.embeddings[0]