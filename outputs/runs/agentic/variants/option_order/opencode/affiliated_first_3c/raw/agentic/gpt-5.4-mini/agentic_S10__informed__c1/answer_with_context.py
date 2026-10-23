from model_client import get_openai_client, model_name
from model_models import ChatResponse, ChatRequest, normalize_text


def answer_with_context(question: str, context: str) -> ChatResponse:
    request = ChatRequest(
        prompt=question,
        context=context,
        system="Answer using only the provided context.",
    )
    client = get_openai_client()
    completion = client.chat.completions.create(
        model=model_name("qa"),
        messages=[
            {"role": "system", "content": request.system},
            {
                "role": "user",
                "content": f"Context:\n{normalize_text(request.context)}\n\nQuestion:\n{normalize_text(request.prompt)}",
            },
        ],
        temperature=request.temperature,
    )
    return ChatResponse(
        text=completion.choices[0].message.content or "", raw=completion
    )
