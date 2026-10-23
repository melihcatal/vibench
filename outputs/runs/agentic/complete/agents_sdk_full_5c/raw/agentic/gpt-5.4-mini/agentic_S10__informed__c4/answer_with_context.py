from __future__ import annotations

from model_client import get_client, load_config, choose_model
from model_models import PromptRequest, response_to_normalized

SYSTEM_PROMPT = "Answer the question using only the supplied context. If the answer is not in the context, say you do not know."


def answer_with_context(context: str, question: str) -> str:
    config = load_config()
    client = get_client(config)
    model = choose_model("answer", config)
    request = PromptRequest(context=context, question=question, system=SYSTEM_PROMPT)
    response = client.chat.completions.create(
        model=model,
        temperature=config.temperature,
        messages=[
            {"role": "system", "content": request.system},
            {"role": "user", "content": f"Context:\n{request.context}\n\nQuestion:\n{request.question}"},
        ],
    )
    return response_to_normalized(response, model).text
