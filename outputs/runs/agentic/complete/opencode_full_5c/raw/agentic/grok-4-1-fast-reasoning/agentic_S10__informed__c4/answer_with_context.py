from model_client import select_model_for_task, get_api_key
from model_models import build_prompt_for_answer
import google.generativeai as genai


def answer_with_context(context: str, question: str) -> str:
    provider, model = select_model_for_task("answer_with_context")
    api_key = get_api_key(provider)
    genai.configure(api_key=api_key)
    gmodel = genai.GenerativeModel(model)
    messages = build_prompt_for_answer(context, question)
    prompt = "\n\n".join(
        [f"{msg['role'].upper()}: {msg['content']}" for msg in messages]
    )
    response = gmodel.generate_content(prompt)
    return response.text
