from typing import List, Dict, Any, Iterator, Union

ChatMessage = Dict[str, Any]
ChatMessages = List[ChatMessage]

# Type hints for OpenAI responses
ChatCompletion = Any
ChatCompletionChunk = Any

def extract_content(response: ChatCompletion) -> str:
    """Normalize response to extract content."""
    return response.choices[0].message.content

def stream_content(stream: Iterator[ChatCompletionChunk]) -> Iterator[str]:
    """Yield content chunks from stream."""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content