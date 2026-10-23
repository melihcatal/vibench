from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os
from typing import Dict, Any, List


def summarize_documents(documents: List[Dict[str, Any]]) -> List[str]:
    """
    Summarizes retrieved document records using Mistral's chat API.
    """
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    summaries = []

    for doc in documents:
        prompt = f"Summarize the following document in 2-3 sentences:\n\n{doc}"
        messages = [ChatMessage(role="user", content=prompt)]

        response = client.chat(model="mistral-large-latest", messages=messages)
        summaries.append(response.choices[0].message.content)

    return summaries
