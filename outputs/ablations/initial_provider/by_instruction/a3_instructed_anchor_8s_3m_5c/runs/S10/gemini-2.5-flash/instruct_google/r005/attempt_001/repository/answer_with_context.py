from model_client import get_generative_model
from model_models import ModelResponse

def answer_with_context(question: str, context: str) -> ModelResponse:
    model = get_generative_model("gemini-pro")
    prompt = f"Using the following context, answer the question.\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"
    response = model.generate_content(prompt)
    return ModelResponse(text=response.text)
