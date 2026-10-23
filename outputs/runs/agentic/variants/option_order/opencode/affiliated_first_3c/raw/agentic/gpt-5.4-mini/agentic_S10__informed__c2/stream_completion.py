from model_client import create_messages, get_client, get_model_name
from model_models import normalize_text


def stream_completion(prompt: str):
    client = get_client()
    stream = client.chat.completions.create(
        model=get_model_name(),
        messages=create_messages(
            "Continue the user's request.", normalize_text(prompt)
        ),
        temperature=0.4,
        max_tokens=512,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
