from model_client import build_client, load_config, select_model_for_task
from model_models import ChatResponse


def answer_with_context(question: str, context: str) -> ChatResponse:
    config = load_config(select_model_for_task("answer"))
    client = build_client(config)
    resp = client.chat.completions.create(
        model=config.model,
        messages=[
            {"role": "system", "content": "Answer using only the provided context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        temperature=0.1,
    )
    return ChatResponse(text=resp.choices[0].message.content, model=config.model, raw=resp)
