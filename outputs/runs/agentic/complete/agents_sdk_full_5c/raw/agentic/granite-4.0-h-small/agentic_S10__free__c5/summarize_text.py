import openai
from model_client import get_openai_client

def summarize_text(text: str, model: str = "gpt-4o-mini") -> str:
    """Summarize long text using OpenAI GPT model.\n\n    Args:\n        text: The input text to summarize.\n        model: Model identifier (default gpt-4o-mini).\n    Returns:\n        A concise summary.\n    """
    client = get_openai_client()
    response = client.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": f"Summarize the following text in no more than 3 sentences:\\n\\n{\\\"text\\\": {\\\"text\\\": text}}},],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()