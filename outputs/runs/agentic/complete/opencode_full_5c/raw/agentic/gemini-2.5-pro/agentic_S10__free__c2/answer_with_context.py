import google.generativeai as genai
from model_client import configure_google_genai
from model_models import ModelRequest, ModelResponse


def answer_with_context(request: ModelRequest) -> ModelResponse:
    configure_google_genai()

    if not request.prompt or not request.context:
        raise ValueError("Prompt and context are required.")

    model_name = request.model or "gemini-pro"
    model = genai.GenerativeModel(model_name)

    prompt = f"Context: {request.context}\n\nQuestion: {request.prompt}\n\nAnswer:"

    response = model.generate_content(prompt)

    return ModelResponse(text=response.text, raw_response=response)
