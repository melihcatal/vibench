from model_client import get_model_client
from model_models import TextResponse


def answer_question(context: str, question: str) -> TextResponse:
    """
    Answers a question based on the provided context.
    """
    model = get_model_client()
    prompt = f"""
    Based on the following context, please answer the question.
    If the context does not provide enough information, say so.

    Context:
    "{context}"

    Question:
    "{question}"
    """
    response = model.generate_content(prompt)

    answer = ""
    finish_reason = None
    if response.parts:
        answer = response.text
    if response.candidates and response.candidates[0].finish_reason:
        finish_reason = response.candidates[0].finish_reason.name

    return TextResponse(text=answer, finish_reason=finish_reason)
