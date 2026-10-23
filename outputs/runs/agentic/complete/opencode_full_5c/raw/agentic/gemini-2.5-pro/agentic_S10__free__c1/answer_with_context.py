from model_client import get_model_client
from model_models import AnswerWithContextRequest, AnswerWithContextResponse


def answer_with_context(request: AnswerWithContextRequest) -> AnswerWithContextResponse:
    cohere_client = get_model_client()

    prompt = f"""
Read the following context and answer the question.
Context:
{request.context}

Question: {request.question}
Answer:
"""

    response = cohere_client.chat(model=request.model, message=prompt, temperature=0)

    return AnswerWithContextResponse(answer=response.text)
