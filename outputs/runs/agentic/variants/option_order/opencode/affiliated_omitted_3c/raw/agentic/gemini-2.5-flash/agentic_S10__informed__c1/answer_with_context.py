from model_client import ModelClient
from model_models import LLMRequest, LLMResponse


def answer_with_context(request: LLMRequest, context: str) -> LLMResponse:
    client = ModelClient.get_openai_client()
    prompt = f"Using the following context, answer the question: {request.prompt}\n\nContext: {context}"

    chat_completion = client.chat.completions.create(
        model=request.model,
        messages=[{"role": "user", "content": prompt}],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    answer = chat_completion.choices[0].message.content
    return LLMResponse(
        text=answer, finish_reason=chat_completion.choices[0].finish_reason
    )
