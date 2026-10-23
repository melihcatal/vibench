from model_client import LLMClientFactory
from model_models import LLMRequest, LLMResponse
import os

def summarize_text(request: LLMRequest) -> LLMResponse:
    client = LLMClientFactory.get_openai_client()
    
    model_id = request.model_id if request.model_id else "gpt-4o"

    messages = [
        {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
        {"role": "user", "content": f"Please summarize the following text:\n\n{request.prompt}"}
    ]

    response = client.chat.completions.create(
        model=model_id,
        messages=messages,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        **request.kwargs
    )

    summary = response.choices[0].message.content
    return LLMResponse(text=summary, model_id=model_id)