from model_client import GeminiClient
from model_models import ModelPayload, ModelResponse

def answer_with_context(payload: ModelPayload) -> ModelResponse:
    client = GeminiClient()
    model = client.get_generative_model(model_name="gemini-pro")
    
    prompt = f"Context: {payload.context}\n\nQuestion: {payload.question}\n\nAnswer:"
    
    response = model.generate_content(prompt)
    
    return ModelResponse(text=response.text)
