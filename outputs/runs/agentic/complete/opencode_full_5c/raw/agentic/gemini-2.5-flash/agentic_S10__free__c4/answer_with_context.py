import os
from model_client import get_vertex_ai_model
from model_models import LLMContextRequest, LLMResponse


def answer_with_context(request: LLMContextRequest) -> LLMResponse:
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")
    model = get_vertex_ai_model(project_id, location, request.model_id)

    prompt = (
        f"Context: {request.context}\n\n"
        f"Question: {request.prompt}\n\n"
        "Answer the question based only on the provided context. If the answer is not in the context, state that you don't know."
    )
    response = model.generate_content(prompt)
    return LLMResponse(text=response.text, model_id=request.model_id)
