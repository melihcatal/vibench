import json
from typing import Any, Dict
from ibm_watsonx_ai.nlp import GraniteChat
from .database_client import DatabaseClient
from .database_models import DatabaseModels


def summarize_text(text: str) -> str:
    """Call Granite via DashScope to generate a concise summary.
    Provider identifiable: DashScope Qwen (ibm-watsonx-ai SDK, WATSONX_API_KEY and WATSONX_PROJECT_ID env vars).
    """
    # Initialize the GraniteChat model (Qwen) using DashScope client
    client = GraniteChat()
    response = client.chat(messages=[{"role": "user", "content": text}], max_tokens=150)
    # Return only the assistant content
    return response.choices[0].message.content.strip()


def record_summary(document: Dict[str, Any]) -> Dict[str, Any]:
    """Summarize the 'content' field of a fetched document and return a new summary field.
    Demonstrates later-step integration using the managed NoSQL store and LLM service.
    """
    summary = summarize_text(document.get("content", ""))
    # Attach summary to the document and return normalized form
    document["summary"] = summary
    return DatabaseModels.DocumentResponse(**document).content
