from model_client import get_openai_client
from model_models import LLMRequest, LLMResponse, ChatMessage


def answer_with_context(question: str, context: str) -> LLMResponse:
    client = get_openai_client()
    prompt_message = ChatMessage(
        role="user",
        content=f"Using the following context, answer the question. Context: {context}\n\nQuestion: {question}",
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": msg.role, "content": msg.content} for msg in [prompt_message]
        ],
        max_tokens=200,
    )
    answer = response.choices[0].message.content.strip()
    return LLMResponse(
        text=answer, model=response.model, usage=response.usage.model_dump()
    )
