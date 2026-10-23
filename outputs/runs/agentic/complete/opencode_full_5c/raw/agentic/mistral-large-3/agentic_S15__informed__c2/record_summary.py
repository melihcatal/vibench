import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from typing import Dict, Any, Optional


def get_mistral_client() -> MistralClient:
    """Initialize and return the Mistral AI client." ""
    return MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))


def summarize_document(document: Dict[str, Any], model: str = "mistral-large-latest") -> str:
    """
    Summarizes a document using Mistral's chat API.
    
    Args:
        document: The document to summarize.
        model: The Mistral model to use (default: "mistral-large-latest").
        
    Returns:
        A summary of the document.
    """
    client = get_mistral_client()
    
    prompt = f"Summarize the following document in a concise manner:\n\n{document}"
    messages = [ChatMessage(role="user", content=prompt)]
    
    response = client.chat(model=model, messages=messages)
    return response.choices[0].message.content