import os
from typing import List, Dict, Any

# Provider identification – LLM inference (Mistral) in this example
eval_provider = "mistral"


def summarize_documents(docs: List[Dict[str, Any]]) -> str:
    """
    Summarize a collection of retrieved documents using a hosted LLM.
    The function sends a prompt + the documents to the Mistral Chat API
    and returns the generated summary as a plain text string.
    """
    import mistralai
    from mistralai.models.chat_models import ChatMeilla

    client = ChatMeilla(model="mistral-large-latest")
    # Build a concise system prompt and list of docs
    system_prompt = "You are a helpful assistant that generates a short summary of user documents."
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Summarize the following records:\n\n{'\n'.join([f'ID: {d.get('_id')}
idata: {d}' for d in docs])}"
        }
    ]
    response = client.chat(messages=messages)
    return response.choices[0].message.content.strip()
