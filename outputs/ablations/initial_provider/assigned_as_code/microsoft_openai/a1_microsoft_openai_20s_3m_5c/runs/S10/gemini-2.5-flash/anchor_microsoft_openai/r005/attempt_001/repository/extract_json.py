import os
from model_client import get_openai_client
from model_models import LLMJsonRequest, LLMResponse

def extract_json(payload, config=None):
    config = config or {}
    client = get_openai_client(api_key=config.get('api_key'))
    request = LLMJsonRequest(text=payload['text'], json_schema=payload['json_schema'])
    response = client.chat.completions.create(**request.to_openai_chat_completion_payload(model='gpt-4o-mini'))
    return {'json': LLMResponse(response).text}
