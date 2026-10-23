from model_client import get_llm_client, select_chat_model
from model_models import normalize_text, summarize_result


def answer_with_context(question: str, context: str) -> str:
    client = get_llm_client()
    model = select_chat_model("qa")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Answer using only the provided context."},
            {"role": "user", "content": f"Context:
{normalize_text(context)}

Question:
{normalize_text(question)}"},
        ],
        temperature=0.1,
    )
    return summarize_result(response)
