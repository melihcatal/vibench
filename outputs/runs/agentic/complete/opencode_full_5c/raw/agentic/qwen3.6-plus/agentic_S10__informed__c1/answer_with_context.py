from model_models import LLMRequest, LLMResponse, build_qa_messages
from model_client import execute_chat


def answer_with_context(
    context: str, question: str, model: str = "mistral-large-latest"
) -> LLMResponse:
    messages = build_qa_messages(context=context, question=question)
    request = LLMRequest(
        model=model,
        messages=messages,
        temperature=0.3,
        max_tokens=1024,
        top_p=0.9,
    )
    return execute_chat(request)
