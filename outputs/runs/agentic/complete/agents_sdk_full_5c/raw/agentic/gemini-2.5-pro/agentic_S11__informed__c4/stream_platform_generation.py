from typing import Iterator
from openai.types.chat import ChatCompletionChunk

from model_client import get_model_client, AZURE_OPENAI_CHAT_DEPLOYMENT_NAME

def stream_generation(prompt: str) -> Iterator[ChatCompletionChunk]:
    """
    Streams the output from a deployed model on Azure OpenAI.

    Args:
        prompt: The user prompt to send to the model.

    Yields:
        The provider's response chunk objects as they are generated.
    """
    client = get_model_client()
    deployment_name = AZURE_OPENAI_CHAT_DEPLOYMENT_NAME

    stream = client.chat.completions.create(
        model=deployment_name, # e.g. "gpt-4o-mini"
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=256,
        stream=True,
    )

    for chunk in stream:
        yield chunk
