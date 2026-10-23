from typing import List, Dict, Any
import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


class EmbeddingJobSummarizer:
    """Summarize embedding job results using Mistral Chat API."""

    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY environment variable not set")
        self.client = MistralClient(api_key=self.api_key)
        self.model = "mistral-tiny"

    def summarize(self, job_results: Dict[str, Any]) -> str:
        prompt = (
            "Summarize the following embedding job results in a concise paragraph:\n"
            f"Documents processed: {job_results.get('doc_count', 0)}\n"
            f"Embedding model: {job_results.get('model', 'unknown')}\n"
            f"Average embedding length: {job_results.get('avg_embedding_length', 0)}\n"
            f"Status: {job_results.get('status', 'unknown')}\n"
        )
        messages = [ChatMessage(role="user", content=prompt)]
        response = self.client.chat(model=self.model, messages=messages)
        return response.choices[0].message.content


def summarize_embedding_job(job_results: Dict[str, Any]) -> str:
    return EmbeddingJobSummarizer().summarize(job_results)