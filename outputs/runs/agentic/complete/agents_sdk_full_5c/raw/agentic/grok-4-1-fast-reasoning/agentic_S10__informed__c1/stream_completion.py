from model_client import get_openai_client
from model_models import mk_user

client = get_openai_client()

def stream_completion(prompt: str):
    """
    Yields partial tokens from the model.
    """
    stream = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[mk_user(prompt)],
        stream=True,
        temperature=0.7
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta is not None:
            yield delta
