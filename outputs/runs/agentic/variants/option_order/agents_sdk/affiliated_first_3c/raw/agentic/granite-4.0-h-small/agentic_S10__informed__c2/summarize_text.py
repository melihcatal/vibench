import os
from model_client import get_llm_client
from model_models import sanitize_response

def summarize_text(text: str) -> str:
    """Summarize long text using a hosted LLM (OpenAI GPT-3.5 Turbo).
    Returns a concise summary.
    """
    client = get_llm_client()
    prompt = f"Summarize the following text in no more than three sentences:\n    {text}"
    response = client.chat_completion(messages=[{"role": "user", "content": prompt}])
    # response assumed to have a 'choices[0].message.content' field
    summary = sanitize_response(response['choices'][0]['message']['content'])
    return summary
