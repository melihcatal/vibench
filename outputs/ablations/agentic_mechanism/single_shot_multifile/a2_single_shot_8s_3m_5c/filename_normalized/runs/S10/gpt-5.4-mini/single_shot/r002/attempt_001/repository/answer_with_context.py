from openai import OpenAI
from model_client import get_client, get_model_name
from model_models import qa_messages, extract_text_output


def answer_with_context(question: str, context: str) -> str:
    client = get_client()
    model = get_model_name("qa")
    messages = qa_messages(question=question, context=context)
    response = client.chat.completions.create(model=model, messages=messages, temperature=0.2)
    return extract_text_output(response)
