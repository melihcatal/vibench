import openai
from model_client import get_openai_client

def spoken_brief(text: str, model: str = "gpt-4o-mini") -> str:
    """Generate a concise spoken brief from text using OpenAI GPT model."""
    client = get_openai_client()
    response = client.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": f"Create a short spoken brief (max 30 seconds) summarizing the following text:\n\n{text}"}],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()
