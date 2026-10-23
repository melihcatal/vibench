from model_client import get_openai_client
from model_models import LLMRequest, LLMResponse, ChatMessage


def summarize_text(text: str) -> LLMResponse:
    client = get_openai_client()
    prompt_message = ChatMessage(
        role="user", content=f"Please summarize the following text concisely: {text}"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": msg.role, "content": msg.content} for msg in [prompt_message]
        ],
        max_tokens=150,
    )
    summary = response.choices[0].message.content.strip()
    return LLMResponse(
        text=summary, model=response.model, usage=response.usage.model_dump()
    )
