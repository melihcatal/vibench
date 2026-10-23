import os
from typing import List, Dict
import anthropic

def summarize_embedding_results(texts_with_embeddings: List[Dict], summary_prompt: str, model: str = "claude-3-opus-20240229") -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")
    
    client = anthropic.Anthropic(api_key=api_key)
    
    context_texts = [item["text"] for item in texts_with_embeddings]
    
    system_message = "You are an AI assistant tasked with summarizing a collection of texts that were processed for an embedding job. Focus on the main topics and key information."
    user_message_content = f"{summary_prompt}\n\nTexts:\n" + "\n".join([f"- {text}" for text in context_texts])
    
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message_content}
        ]
    )
    return response.content[0].text
