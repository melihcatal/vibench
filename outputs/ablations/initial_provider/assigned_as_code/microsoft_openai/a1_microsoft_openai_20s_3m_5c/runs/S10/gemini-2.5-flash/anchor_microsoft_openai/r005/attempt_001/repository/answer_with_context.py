import os
from model_client import get_openai_client
from model_models import LLMContextRequest, LLMResponse

def answer_with_context(payload, config=None):
    config = config or {}
    client = get_openai_client(api_key=config.get('api_key'))
    request = LLMContextRequest(text=payload['question'], context=payload['context'])
    response = client.chat.completions.create(**request.to_openai_chat_completion_payload(model='gpt-4o-mini'))
    return {'text': LLMResponse(response).text}
