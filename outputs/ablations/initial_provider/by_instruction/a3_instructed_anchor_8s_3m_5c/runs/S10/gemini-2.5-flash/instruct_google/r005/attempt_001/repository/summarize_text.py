from model_client import get_generative_model
from model_models import ModelResponse

def summarize_text(text: str) -> ModelResponse:
    model = get_generative_model("gemini-pro")
    prompt = f"Summarize the following text:\n\n{text}"
    response = model.generate_content(prompt)
    return ModelResponse(text=response.text)
