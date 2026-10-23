from model_client import complete
from model_models import LLMRequest, Message


def answer_with_context(
    question: str, context: str, model_family: str = "claude-3-5-sonnet-20241022"
) -> str:
    request = LLMRequest(
        model_family=model_family,
        messages=[
            Message(
                role="user",
                content=f"Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer using only the context when possible.",
            )
        ],
        temperature=0.2,
        max_tokens=400,
    )
    return complete(request)
