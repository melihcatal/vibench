import os
from model_client import LLMClient

def summarize_text(text: str) -> str:
    """Summarize long input text using the hosted OpenAI GPT-4 model.

    Args:
        text: The source text to summarize.
    
    Returns:
        A concise human‑readable summary.
    """
    client = LLMClient(model="gpt-4")  # OpenAI provider signal
    prompt = "Summarize the following text in three sentences:\n\n" + text
    return client.chat_completion(prompt=prompt)['choices'][0]['message']['content']