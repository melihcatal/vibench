import os
from typing import List, Dict
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

def summarize_transcription(segments: List[Dict[str, str]], model: str = "mistral-tiny") -> str:
    """
    Summarizes transcription segments using Mistral Chat API.
    Returns a concise summary of the transcript.
    """
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable not set.")
    
    client = MistralClient(api_key=api_key)
    
    text = " \n".join([segment["text"] for segment in segments])
    
    messages = [
        ChatMessage(
            role="user",
            content=f"Summarize the following transcript:\n\n{text}"
        )
    ]
    
    response = client.chat(
        model=model,
        messages=messages
    )
    
    return response.choices[0].message.content