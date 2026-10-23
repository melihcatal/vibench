from openai import OpenAI
from model_client import get_client, get_model_name
from model_models import QARequest, QAResult


def answer_with_context(question: str, context: str, *, model: str | None = None) -> QAResult:
    client = get_client()
    model_name = model or get_model_name("qa")
    request = QARequest(question=question, context=context)
    response = client.responses.create(model=model_name, input=request.to_prompt())
    output_text = response.output_text if hasattr(response, "output_text") else str(response)
    return QAResult.from_text(output_text, model=model_name)
