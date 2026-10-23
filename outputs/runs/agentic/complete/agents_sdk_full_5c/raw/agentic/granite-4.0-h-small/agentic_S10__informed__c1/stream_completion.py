import os
import openai
from model_client import get_openai_api_key

def stream_completion(prompt: str, model_id: str = "gpt-4o-mini"):
    """Stream partial output tokens from OpenAI GPT model.

    Args:
        prompt: Initial prompt to start streaming.
        model_id: Identifier for the OpenAI model family.
    """
    openai.api_key = get_openai_api_key()
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        temperature=0.7,
    )
    for chunk in response:
        data = chunk.choices[0].delta
        if "content" in data:
            yield data["content"]
        elif "finish_reason" in data:
            break

if __name__ == "__main__":
    prompt = "Explain how a neural network works in short paragraphs."
    for fragment in stream_completion(prompt):
        print(fragment, end='')
