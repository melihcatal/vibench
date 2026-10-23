import os
from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from typing import Union, Generator
from model_models import ChatCompletionRequest

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_chat_completion(
    request: ChatCompletionRequest,
    stream: bool = False,
) -> Union[ChatCompletion, Generator[ChatCompletionChunk, None, None]]:
    data = request.model_dump(exclude_none=True)
    data["stream"] = stream
    response = client.chat.completions.create(**data)
    return response