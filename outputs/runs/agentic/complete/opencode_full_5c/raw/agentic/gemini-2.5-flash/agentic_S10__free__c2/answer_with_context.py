from model_client import VertexAIModelClient
from model_models import QuestionAnsweringRequest, QuestionAnsweringResponse


def answer_with_context(request: QuestionAnsweringRequest) -> QuestionAnsweringResponse:
    client = VertexAIModelClient()
    return client.answer_with_context(request)
