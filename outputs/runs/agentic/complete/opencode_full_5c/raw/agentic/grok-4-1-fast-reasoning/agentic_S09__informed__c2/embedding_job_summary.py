import os
from typing import Dict, Any
from mistralai.client import Mistral


def embedding_job_summary(embedding_response: Dict[str, Any]) -> str:
    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
    num_embeddings = len(embedding_response["data"])
    model_used = embedding_response["model"]
    usage = embedding_response.get("usage", {})
    prompt = f"""Summarize this embedding job result in one sentence:

- Model: {model_used}
- Number of embeddings: {num_embeddings}
- Usage: {usage}"""
    chat_response = client.chat(
        model="mistral-large-latest", messages=[{"role": "user", "content": prompt}]
    )
    return chat_response.choices[0].message.content
