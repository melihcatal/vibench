from model_client import ModelClient
from model_models import LLMRequest, LLMResponse

def summarize_text(request: LLMRequest) -> LLMResponse:
    client = ModelClient.get_openai_client()
    prompt = f"Please summarize the following text:
\n{request.prompt}"

    chat_completion = client.chat.completions.create(
        model=request.model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=request.temperature,
        max_tokens=request.max_tokens
    )

    summary = chat_completion.choices[0].message.content
    return LLMResponse(text=summary, finish_reason=chat_completion.choices[0].finish_reason)
