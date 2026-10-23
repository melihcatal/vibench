from model_client import client

def stream_completion(prompt: str):
    """
    Streams partial output tokens from a hosted LLM.
    Usage: for token in stream_completion(prompt): print(token, end="")
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in response:
        delta = chunk.choices[0].delta.content
        if delta is not None:
            yield delta