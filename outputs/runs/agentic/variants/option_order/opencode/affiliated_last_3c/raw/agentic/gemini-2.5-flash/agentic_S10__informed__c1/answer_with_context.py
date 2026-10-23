from model_client import OpenAIClient
from model_models import LLMResponse, ContextAnswerRequest


def answer_with_context(request: ContextAnswerRequest) -> LLMResponse:
    client = OpenAIClient().get_client()
    response = client.chat.completions.create(
        model=request.model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions based on provided context.",
            },
            {
                "role": "user",
                "content": f"Context: {request.context}\n\nQuestion: {request.question}",
            },
        ],
        max_tokens=1024,
        temperature=0.2,
    )
    return LLMResponse(
        generated_text=response.choices[0].message.content,
        finish_reason=response.choices[0].finish_reason,
    )
