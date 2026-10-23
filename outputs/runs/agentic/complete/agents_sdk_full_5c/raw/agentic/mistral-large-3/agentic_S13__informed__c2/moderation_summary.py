"""
Summarize moderation decisions using Mistral Chat API.
"""
from typing import List, Dict

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))


def summarize_moderation_decisions(decisions: List[Dict]) -> str:
    """Summarize moderation decisions using Mistral."""
    decision_texts = "\n".join(
        f"Text: {d['text']} | Decision: {d['decision']} | Categories: {', '.join([c['category'] for c in d['categories'] if c['label'] == 'flagged'])}"
        for d in decisions
    )
    
    messages = [
        ChatMessage(
            role="user",
            content=f"Summarize the following moderation decisions in a concise report:\n\n{decision_texts}"
        )
    ]
    
    response = client.chat(
        model="mistral-tiny",
        messages=messages
    )
    
    return response.choices[0].message.content