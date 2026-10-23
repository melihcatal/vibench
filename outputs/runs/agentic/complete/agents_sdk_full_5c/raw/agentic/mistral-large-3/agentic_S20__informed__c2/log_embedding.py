"""Embed selected log messages for semantic retrieval using OpenAI Embeddings."""

import os
from typing import List

from openai import OpenAI
from observability_models import LogEntry


class LogEmbedder:
    """Embed log messages using OpenAI Embeddings."""

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def embed_message(self, message: str) -> List[float]:
        """Generate an embedding for a log message."""
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=message,
        )
        return response.data[0].embedding

    def embed_logs(self, log_entries: List[LogEntry]) -> List[List[float]]:
        """Generate embeddings for a list of log messages."""
        return [self.embed_message(entry.message) for entry in log_entries]


if __name__ == "__main__":
    from fetch_recent_logs import fetch_recent_logs
    
    logs = fetch_recent_logs(service="support-service", user_id="67890")
    embedder = LogEmbedder()
    embeddings = embedder.embed_logs(logs)
    
    for log, embedding in zip(logs, embeddings):
        print(f"Log: {log.message[:50]}... | Embedding length: {len(embedding)}")