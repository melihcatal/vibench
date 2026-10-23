import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from typing import List, Dict, Any

client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))


def summarize_embedding_job(job_id: str, results: List[Dict[str, Any]]) -> str:
    """Summarize embedding job results using Mistral Chat API."""
    summary_prompt = (
        f"Summarize the embedding job {job_id} with the following results:\n"
        f"{results}\n\n"
        "Provide a concise summary of the job, including the number of embeddings generated, "
        "any notable patterns, and potential next steps."
    )

    messages = [ChatMessage(role="user", content=summary_prompt)]
    response = client.chat(model="mistral-large-latest", messages=messages)
    return response.choices[0].message.content
