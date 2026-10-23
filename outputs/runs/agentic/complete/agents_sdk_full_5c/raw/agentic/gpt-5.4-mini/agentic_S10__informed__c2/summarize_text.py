from model_client import build_client, load_config, select_model_for_task
from model_models import ChatRequest, ChatResponse


def summarize_text(long_text: str) -> ChatResponse:
    config = load_config(select_model_for_task("summarize"))
    client = build_client(config)
    req = ChatRequest(
        prompt=f"Summarize the following text in a concise paragraph:\n\n{long_text}",
        model=config.model,
        system="You are a helpful summarization assistant.",
    )
    resp = client.chat.completions.create(
        model=req.model,
        messages=[
            {"role": "system", "content": req.system},
            {"role": "user", "content": req.prompt},
        ],
        temperature=req.temperature,
    )
    return ChatResponse(text=resp.choices[0].message.content, model=req.model, raw=resp)
