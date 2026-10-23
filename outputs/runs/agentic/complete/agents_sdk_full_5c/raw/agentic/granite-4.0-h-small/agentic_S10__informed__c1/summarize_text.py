import os
import openai
from model_client import get_openai_api_key

def summarize_text(text: str, model_id: str = "gpt-4o-mini") -> str:
    """Summarize long text using OpenAI GPT model.

    Args:
        text: The long input text.
        model_id: Identifier for the OpenAI model family.
    """
    openai.api_key = get_openai_api_key()
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=[{"role": "user", "content": f"Summarize the following text in no more than 3 sentences: {text}"}],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    sample = "Python is a high-level programming language. It emphasizes code readability with its notable use of significant whitespace. Its language constructs as well as its object-oriented approach aim to help programmers write clear, logical code for small and large-scale projects."
    print(summarize_text(sample))
