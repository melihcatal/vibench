from model_client import get_client, select_model, chat_messages
from model_models import LLMRequest, LLMResponse, normalize_text


def summarize_text(text: str) -> LLMResponse:
    req = LLMRequest(prompt=normalize_text(text))
    client = get_client()
    model = select_model("summarize")
    resp = client.chat.completions.create(
        model=model,
        messages=chat_messages("Summarize the provided text concisely.", req.prompt),
    )
    return LLMResponse(text=resp.choices[0].message.content or "", model=model)
