from model_client import get_client, select_model, chat_messages
from model_models import LLMRequest, LLMResponse, normalize_text


def answer_with_context(question: str, context: str) -> LLMResponse:
    req = LLMRequest(prompt=normalize_text(question), context=normalize_text(context))
    client = get_client()
    model = select_model("answer")
    resp = client.chat.completions.create(
        model=model,
        messages=chat_messages(
            "Answer the question using only the provided context.",
            req.prompt,
            req.context,
        ),
    )
    return LLMResponse(text=resp.choices[0].message.content or "", model=model)
