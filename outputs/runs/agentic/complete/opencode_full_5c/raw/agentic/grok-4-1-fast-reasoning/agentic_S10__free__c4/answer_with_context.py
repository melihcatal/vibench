from model_client import get_llm_client, get_model_id
from model_models import build_qa_prompt, parse_chat_completion


def answer_with_context(
    question: str, context: str, model_family: str = "gpt-4o-mini"
) -> str:
    client = get_llm_client()
    model = get_model_id(model_family)
    messages = build_qa_prompt(context, question)
    response = client.chat.completions.create(
        model=model, messages=messages, temperature=0.1
    )
    return parse_chat_completion(response)
