from model_client import call_gemini_generate_content
from model_models import AnswerWithContextRequest, LLMResponse


def answer_with_context(
    question: str, context: str, model_name: str = "gemini-pro"
) -> LLMResponse:
    prompt = f"Answer the following question based on the provided context.\n\nContext: {context}\nQuestion: {question}\nAnswer:"
    request = AnswerWithContextRequest(
        prompt=prompt, context=context, question=question, model_name=model_name
    )
    return call_gemini_generate_content(request)
