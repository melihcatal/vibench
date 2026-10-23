from typing import Generator
from model_client import get_openai_client
from model_models import StreamCompletionInput, StreamCompletionOutputChunk

def stream_completion(input_data: StreamCompletionInput) -> Generator[StreamCompletionOutputChunk, None, None]:
    client = get_openai_client()
    messages = [
        {"role": "user", "content": input_data.prompt}
    ]
    stream = client.chat.completions.create(
        model=input_data.model_name,
        messages=messages,
        max_tokens=input_data.max_tokens,
        temperature=input_data.temperature,
        stream=True
    )
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield StreamCompletionOutputChunk(
                token=chunk.choices[0].delta.content,
                finish_reason=chunk.choices[0].finish_reason
            )
        elif chunk.choices and chunk.choices[0].finish_reason:
            yield StreamCompletionOutputChunk(
                token="",
                finish_reason=chunk.choices[0].finish_reason
            )