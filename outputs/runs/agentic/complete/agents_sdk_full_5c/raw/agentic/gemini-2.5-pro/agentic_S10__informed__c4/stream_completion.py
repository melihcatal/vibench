from typing import Iterator
from model_client import get_model_client

def stream_completion(prompt: str) -> Iterator[str]:
    """
    Streams partial completions from the OpenAI API.

    Args:
        prompt: The prompt to send to the model.

    Yields:
        A stream of text chunks from the model's response.
    """
    client = get_model_client()
    
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        stream=True,
    )
    
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content is not None:
            yield content
