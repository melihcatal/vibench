import os
from model_client import get_openai_client
from model_models import LLMRequest, LLMStreamResponse

def stream_completion(payload, config=None):
    config = config or {}
    client = get_openai_client(api_key=config.get('api_key'))
    request = LLMRequest(text=payload['text'])
    stream = client.chat.completions.create(stream=True, **request.to_openai_chat_completion_payload(model='gpt-4o-mini'))
    for chunk in stream:
        yield {'text': LLMStreamResponse(chunk).text}
